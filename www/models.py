# Create your models here.
import markdown
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    content_md = models.TextField()
    content_html = models.TextField()


def pre_save_post_receiver(sender, instance: Post, *args, **kwargs):
    if not instance.content_md:
        instance.content_md = ''
    instance.content_html = markdown.markdown(instance.content_md)


pre_save.connect(pre_save_post_receiver, sender=Post)
