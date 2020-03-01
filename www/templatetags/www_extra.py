from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def fa(name):
    return mark_safe(f'<i class="fa fa-{name}" aria-hidden="true"></i>')
