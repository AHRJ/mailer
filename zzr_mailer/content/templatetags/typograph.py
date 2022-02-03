from chakert import Typograph
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def typograph(value):
    return mark_safe(Typograph.typograph_html(value, lang="ru"))
