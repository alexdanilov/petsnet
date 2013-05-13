from django import template
from system.models import Banner


register = template.Library()


@register.simple_tag(name='banner')
def get_banner(code):
    "Get random banner by given banner-code"
    content = ''
    items = Banner.objects.filter(visibility=True, code=code).order_by('?')
    if items.count() > 0:
        content = items[0].content
    return content
