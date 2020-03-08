import random

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from utils import login_code_manager

LOGIN_CODE_CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'r', 's', 't', 'u', 'v', 'x',
                    'y', 'z', '2', '3', '4', '5', '6', '8']

SESSION_KEY_LOGIN_CODE = 'landzero:login-code'


def before_sign_in(request):
    if not request.user.is_authenticated:
        # ensure login code
        login_code = request.session.get(SESSION_KEY_LOGIN_CODE)
        if login_code:
            # validate the login code
            user_id = login_code_manager.get_code_user(login_code)
            if user_id:
                # login the user
                login(request, User.objects.get(id=int(user_id)))
                # unmark the code
                login_code_manager.unmark_code(login_code)
                # delete the code_user
                login_code_manager.delete_code_user(login_code)
            else:
                # extend the mark
                login_code_manager.mark_code(login_code)
        else:
            # create the login code
            login_code = ''.join(random.choice(LOGIN_CODE_CHARS) for _ in range(16))
            # save to session
            request.session[SESSION_KEY_LOGIN_CODE] = login_code
            # extend the mark
            login_code_manager.mark_code(login_code)

    if request.user.is_authenticated:
        # delete session login code
        request.session.delete(SESSION_KEY_LOGIN_CODE)


def signed_in(request):
    before_sign_in(request)
    return JsonResponse({'signed_in': request.user.is_authenticated})


def sign_in(request):
    before_sign_in(request)

    if request.user.is_authenticated:
        return redirect('index')

    return render(request, 'www/sign_in.html', {'login_code': request.session.get(SESSION_KEY_LOGIN_CODE)})
