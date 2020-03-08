# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.utils import check_signature


@csrf_exempt
def callback_mp(request: HttpRequest):
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']

    try:
        check_signature(
            token=settings.WEIXIN_MP['APP_TOKEN'],
            signature=signature,
            timestamp=timestamp,
            nonce=nonce,
        )
    except InvalidSignatureException as e:
        return HttpResponse(status=403, content='invalid signature', content_type='text/plain')

    if request.method == 'GET':
        echo_str = request.GET['echostr']
        return HttpResponse(echo_str, content_type='text/plain')
    else:
        encrypt_type = request.GET['encrypt_type']
        msg_signature = request.GET['msg_signature']
        crypto = WeChatCrypto(
            token=settings.WEIXIN_MP['APP_TOKEN'],
            encoding_aes_key=settings.WEIXIN_MP['APP_AES_KEY'],
            app_id=settings.WEIXIN_MP['APP_ID'],
        )
        try:
            raw_msg = crypto.decrypt_message(
                msg=request.body,
                signature=msg_signature,
                timestamp=timestamp,
                nonce=nonce,
            )
        except (InvalidSignatureException, InvalidAppIdException):
            return HttpResponse(status=403, content='invalid message', content_type='text/plain')
        msg = parse_message(raw_msg)
        if msg.type == 'text':
            reply = create_reply(msg.content, msg)
            reply_msg = crypto.encrypt_message(reply.render(), nonce, timestamp)
            return HttpResponse(reply_msg, content_type='application/xml')
        else:
            return HttpResponse('success', content_type='text/plain')
