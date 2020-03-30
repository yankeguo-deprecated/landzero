from django.shortcuts import render

from www.models import Post


def index(request):
    posts = Post.objects.order_by('-timestamp')
    return render(request, 'www/index.html', {'posts': posts})
