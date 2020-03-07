# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature


@csrf_exempt
def callback_mp(request: HttpRequest):
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    echostr = request.GET['echostr']

    try:
        check_signature(token=settings.WEIXIN_MP['APP_TOKEN'], signature=signature, timestamp=timestamp, nonce=nonce)
    except InvalidSignatureException as e:
        return HttpResponse(status=403, content='invalid signature', content_type='text/plain')

    if request.method == 'GET':
        return HttpResponse(echostr, content_type='text/plain')
    else:
        encrypt_type = request.GET['encrypt_type']
        msg_signature = request.GET['msg_signature']
        return HttpResponse('success', content_type='text/plain')
