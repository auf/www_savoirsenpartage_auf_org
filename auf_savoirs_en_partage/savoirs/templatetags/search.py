#coding: utf-8

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

EXCERPT_LENGTH = 200

@register.filter
def highlight(text, regexp=None, autoescape=None):
    """Met en évidence les parties du texte qui correspondent à l'expression
       régulière passée en argument."""
    if autoescape:
        text = conditional_escape(text)
    if regexp:
        text = regexp.sub(r'<b>\g<0></b>', text)
    return mark_safe(text)

@register.filter
def excerpt(text, regexp=None):
    """Tronque le texte autour de la première correspondance de l'expression
       régulière."""
    if len(text) <= EXCERPT_LENGTH:
        return text
    m = regexp is not None and regexp.search(text)
    if m:
        pos = m.start()
        end_of_sentence = max(text.rfind('.', 0, pos), text.rfind('?', 0, pos), text.rfind('!', 0, pos))
        start = end_of_sentence + 1 if end_of_sentence != -1 else 0
        end = pos + EXCERPT_LENGTH
    else:
        start = 0
        end = start + EXCERPT_LENGTH
    if end < len(text) - 1:
        try:
            end = text.rindex(' ', start, end)
        except ValueError:
            pass
    excerpt = text[start:end].strip()
    if start > 0:
        excerpt = '(...) ' + excerpt
    if end < len(text) - 1:
        excerpt += ' (...)'
    return excerpt
excerpt.is_safe = True
