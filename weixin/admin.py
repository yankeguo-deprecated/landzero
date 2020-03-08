from django.contrib import admin

from .models import OpenId


class OpenIdAdmin(admin.ModelAdmin):
    list_display = ['open_id', 'user']
    readonly_fields = ['user']


admin.site.register(OpenId, OpenIdAdmin)
