from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, regexp, autoescape=None):
    """Met en évidence les parties du texte qui correspondent à l'expression
       régulière passée en argument."""
    if autoescape:
        text = conditional_escape(text)
    if words:
        text = words.sub(r'<b>\g<0></b>', text)
    return mark_safe(text)
