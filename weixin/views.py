# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.utils import check_signature

from utils import login_code_manager
from .models import OpenId


def __handle_text(open_id: OpenId, content: str):
    cleaned = content.replace(' ', '').lower()
    if cleaned.startswith("l"):
        login_code = cleaned[1:]
        if login_code_manager.has_code(login_code):
            login_code_manager.set_code_user(login_code, str(open_id.user_id))
            return '登录成功，请刷新页面'
        else:
            return '没有找到登录代码，请检查是否输入正确'

    return f'User#{open_id.user_id}: {content}'


def __success_response():
    return HttpResponse(content='success', content_type='text/plain')


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

        open_id = OpenId.objects.find_or_create(open_id=msg.source)

        if msg.type == 'text':
            res = __handle_text(open_id, str(msg.content).strip())
            if res:
                reply = create_reply(res, msg)
                reply_msg = crypto.encrypt_message(reply.render(), nonce, timestamp)
                return HttpResponse(content=reply_msg, content_type='application/xml')
            else:
                return __success_response()
        else:
            return __success_response()
