# coding: utf-8

from django import template

from chercheurs.models import GroupeChercheur, DomaineRecherche, CG_STATUT_CHOICES
from chercheurs.templatetags.chercheurs_admin import prepare_choices

register = template.Library()

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_statut(context):
    return {'title': 'statut',
            'choices': prepare_choices(CG_STATUT_CHOICES, 'statut', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_groupe_chercheurs(context):
    return {'title': u"communautés de chercheurs",
            'choices': prepare_choices(GroupeChercheur.objects.values_list('id', 'nom'), 'groupe', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_domaine_recherche(context):
    return {'title': u"domaine de recherche",
            'choices': prepare_choices(DomaineRecherche.objects.values_list('id', 'nom'), 'groupe', context)}

