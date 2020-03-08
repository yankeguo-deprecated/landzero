import random

from django.shortcuts import render

from utils import login_code_manager

LOGIN_TOKEN_CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'r', 's', 't', 'u', 'v', 'x',
                     'y', 'z', '2', '3', '4', '5', '6', '8']

KEY_LOGIN_CODE = 'landzero:login-code'


def index(request):
    return render(request, 'www/index.html', {})


def sign_in(request):
    # initialize login code
    if not request.session.get(KEY_LOGIN_CODE):
        request.session[KEY_LOGIN_CODE] = ''.join(random.choice(LOGIN_TOKEN_CHARS) for _ in range(16))
    login_code = request.session[KEY_LOGIN_CODE]

    # find user_id
    login_code_manager.mark_code(login_code)
    user_id = login_code_manager.get_code(login_code)
    return render(request, 'www/sign_in.html', {'login_code': login_code, 'user_id': user_id})
