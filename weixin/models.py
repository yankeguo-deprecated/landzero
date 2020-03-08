# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class OpenIdManager(models.Manager):

    def find_or_create(self, open_id):
        try:
            return self.model.objects.get(open_id=open_id)
        except self.model.DoesNotExist:
            user = User.objects.create_user(username='wx_' + open_id, first_name='用户')
            return self.model.objects.create(user=user, open_id=open_id)


class OpenId(models.Model):
    objects = OpenIdManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    open_id = models.CharField(max_length=128, unique=True)
