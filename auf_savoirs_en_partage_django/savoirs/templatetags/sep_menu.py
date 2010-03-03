# -*- encoding: utf-8 -*-
from django import template
from savoirs.models import Discipline



def sep_menu ():
    disciplines = Discipline.objects.all ()
    return {'disciplines': disciplines}

register = template.Library()
register.inclusion_tag('menu.html')(sep_menu)
