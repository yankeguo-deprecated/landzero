from django.shortcuts import render


def index(request):
    return render(request, 'www/index.html', {})


def sign_in(request):
    return render(request, 'www/sign_in.html', {})
