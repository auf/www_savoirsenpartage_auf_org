# -*- coding: utf-8 -*-

from selectable.base import ModelLookup
from selectable.registry import registry

from chercheurs.models import Chercheur


class ChercheurLookup(ModelLookup):
    model = Chercheur
    search_field = 'nom__icontains'

registry.register(ChercheurLookup)
