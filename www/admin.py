# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'slug', 'timestamp']
    raw_id_fields = ['user']
    readonly_fields = ['content_html_preview']
    exclude = ['content_html']

    def content_html_preview(self, obj):
        return mark_safe(obj.content_html)


admin.site.register(Post, PostAdmin)
