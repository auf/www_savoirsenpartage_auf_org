# -*- encoding: utf-8 -*-
from django import template
from datamaster_modeles.models import Region
from savoirs.models import Discipline

def sep_menu ():
    regions = Region.objects.filter(actif=True).order_by('nom')
    disciplines = Discipline.objects.all()
    return {'disciplines': disciplines, 'regions':regions}

register = template.Library()
register.inclusion_tag('menu.html')(sep_menu)
