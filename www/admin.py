# Register your models here.
from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'slug', 'timestamp']
    raw_id_fields = ['user']
    readonly_fields = ['content_html']


admin.site.register(Post, PostAdmin)
