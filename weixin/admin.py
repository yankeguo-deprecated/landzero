from django.contrib import admin

from .models import OpenId


class OpenIdAdmin(admin.ModelAdmin):
    pass


admin.site.register(OpenId, OpenIdAdmin)
