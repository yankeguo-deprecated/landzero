# Create your views here.
from django.http import HttpResponse


def callback_mp(request):
    return HttpResponse('hello, world', content_type='text/plain')
