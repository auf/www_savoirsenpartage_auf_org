# -*- encoding: utf-8 -*-
from django import forms
from models import *
from models import Utilisateur
from savoirs.forms import SEPDateField
from models import STATUT_CHOICES

class PersonneForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe") 
    genre = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENRE_CHOICES)
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'courriel', 'password', 'genre')
        
class GroupeForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('groupes',)

class ChercheurForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('statut', 'diplome', )
        
class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'revue', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
class TheseForm(PublicationForm):
    titre = forms.CharField(required=True, label="Titre de la thèse ou du mémoire")
    annee = forms.IntegerField(required=True, label="Année de soutenance (réalisée ou prévue)")
    editeur = forms.CharField(required=False, label="Directeur de thèse")
    lieu_edition = forms.CharField(required=False, label="Établissement de soutenance")
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
class ExpertiseForm(forms.ModelForm):
    date = SEPDateField(required=False, label="Date")
    class Meta:
        model = Expertise
        fields = ('nom', 'date', 'organisme_demandeur', 'organisme_demandeur_visible')        

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('etablissement',)
    def clean(self):
        cleaned_data = self.cleaned_data
        statut = self.data.get('chercheur-statut')
        etablissement = self.cleaned_data.get("etablissement")
        etablissement_autre_nom = self.data.get("etablissement_autre-etablissement_autre_nom")
        if statut == "enseignant":
            if not etablissement and not etablissement_autre_nom:
                raise forms.ValidationError("")
        return cleaned_data

class EtablissementAutreForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('etablissement_autre_nom', 'etablissement_autre_pays' )

class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('discipline', 'theme_recherche', 'mots_cles', 'url_site_web', 'url_blog',)
        
class PersonneEditForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ('nom', 'prenom', 'genre') 

class RepertoireSearchForm (forms.Form):
    mots_cles = forms.CharField (required = False, label="Mots-clés")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Tous")
    domaine = forms.ModelChoiceField(queryset=Groupe.objects.all(), required=False, label="Domaine de recherche", empty_label="Tous")
    statut = forms.ChoiceField(choices=(('','Tous'),)+STATUT_CHOICES+(('expert','Expert'),), required=False, label="Statut")
    pays = forms.ModelChoiceField(queryset=Pays.objects.all().order_by("nom"), required=False, label="Localisation", empty_label="Tous")
      
class SendPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label="courriel")
    def clean_email(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        if email:
            try:
                Utilisateur.objects.get(courriel=email)
            except:
                raise forms.ValidationError("Ce courriel n'existe pas dans notre base de données.")       
        return email

class NewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Mot de passe") 
    password_repeat = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirmez mot de passe")
    def clean_password_repeat(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError("Les mots de passe ne concordent pas")
        return password_repeat   

