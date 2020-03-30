from django.shortcuts import render
from django.utils.safestring import mark_safe

from www.models import Post


def view_post(request, slug):
    post = Post.objects.get(slug=slug)
    content = mark_safe(post.content_html)
    return render(request, 'www/view_post.html', {'post': post, 'content': content})
