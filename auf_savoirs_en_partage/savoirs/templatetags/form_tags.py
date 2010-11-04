# -*- encoding: utf-8 -*-
from django import template

register = template.Library()

@register.inclusion_tag('render_field.html')
def form_field(field):
    return dict(field=field)
