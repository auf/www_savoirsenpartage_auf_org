# coding: utf-8

from django import template
from django.utils.encoding import smart_unicode

from chercheurs.models import GroupeChercheur, DomaineRecherche, GENRE_CHOICES, STATUT_CHOICES
from datamaster_modeles.models import Region, Pays
from savoirs.models import Discipline

register = template.Library()

OUI_NON_CHOICES = [(1, 'Oui'), (0, 'Non')]

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_genre(context):
    return {'title': 'genre',
            'choices': prepare_choices(GENRE_CHOICES, 'genre', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_statut(context):
    return {'title': 'statut',
            'choices': prepare_choices(STATUT_CHOICES, 'statut', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_membre_reseau_institutionnel(context):
    return {'title': u"appartenance aux instances d'un réseau institutionnel de l'AUF",
            'choices': prepare_choices(OUI_NON_CHOICES, 'membre_reseau_institutionnel', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_membre_instance_auf(context):
    return {'title': u"appartenance à une instance de l'AUF",
            'choices': prepare_choices(OUI_NON_CHOICES, 'membre_instance_auf', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_discipline(context):
    return {'title': u"discipline",
            'choices': prepare_choices(Discipline.objects.values_list('id', 'nom'), 'discipline', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_region(context):
    return {'title': u"région",
            'choices': prepare_choices(Region.objects.values_list('id', 'nom'), 'region', context, remove=['pays', 'nord_sud'])}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_nord_sud(context):
    return {'title': u'nord/sud',
            'choices': prepare_choices([('Nord', 'Nord'), ('Sud', 'Sud')], 'nord_sud', context, remove=['pays', 'region'])}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_pays(context):
    request = context['request']
    region = request.GET.get('region')
    nord_sud = request.GET.get('nord_sud')
    choices = Pays.objects
    if region is not None:
        choices = choices.filter(region=region)
    elif nord_sud is not None:
        choices = choices.filter(nord_sud=nord_sud)
    return {'title': u"pays",
            'choices': prepare_choices(choices.values_list('code', 'nom'), 'pays', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_groupe_chercheurs(context):
    return {'title': u"communautés de chercheurs",
            'choices': prepare_choices(GroupeChercheur.objects.values_list('id', 'nom'), 'groupes', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_domaine_recherche(context):
    return {'title': u"domaine de recherche",
            'choices': prepare_choices(DomaineRecherche.objects.values_list('id', 'nom'), 'groupes', context)}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_expert(context):
    return {'title': u"expert",
            'choices': prepare_choices(OUI_NON_CHOICES, 'expert', context)}

def prepare_choices(choices, query_param, context, remove=[]):
    request = context['request']
    cl = context['cl']
    query_val = request.GET.get(query_param)
    result = [{'selected': query_val is None,
               'query_string': cl.get_query_string({}, [query_param] + remove),
               'display': 'Tout'}]
    for k, v in choices:
        result.append({'selected': smart_unicode(k) == query_val,
                       'query_string': cl.get_query_string({query_param: k}, remove),
                       'display': v})
    return result
