# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms

from selectable import forms as selectable

from models import FaunAuteur
from lookups import ChercheurLookup


class FaunAuteurForm(forms.ModelForm):
    sep_chercheur = selectable.AutoComboboxSelectField(lookup_class=ChercheurLookup, allow_new=False, label="SEP Chercheur")

    class Meta:
        model = FaunAuteur
        exclude = ('sep_chercheur',)

    def __init__(self, *args, **kwargs):
        super(FaunAuteurForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.sep_chercheur:
            self.initial['sep_chercheur'] = self.instance.sep_chercheur

    def save(self, *args, **kwargs):
        sep_chercheur = self.cleaned_data['sep_chercheur']
        self.instance.sep_chercheur = sep_chercheur
        return super(FaunAuteurForm, self).save(*args, **kwargs)


class FaunAuteurAdmin(admin.ModelAdmin):
    form = FaunAuteurForm
admin.site.register(FaunAuteur, FaunAuteurAdmin)
