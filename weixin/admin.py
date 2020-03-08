from django.contrib import admin

from .models import OpenId


class OpenIdAdmin(admin.ModelAdmin):
    list_display = ['id', 'open_id', 'user']
    raw_id_fields = ['user']


admin.site.register(OpenId, OpenIdAdmin)
