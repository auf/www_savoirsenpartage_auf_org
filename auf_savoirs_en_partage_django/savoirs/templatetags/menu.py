# -*- encoding: utf-8 -*-
from django import template
from savoirs.models import Discipline


register = template.Library()

@register.inclusion_tag('menu.html',takes_context=True)
def sep_menu ():
    disciplines = Discipline.objects.all ()
    print disciplines
    return {'disciplines': disciplines}

