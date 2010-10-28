# -*- encoding: utf-8 -*-
from django import forms
from models import *
from models import Utilisateur

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
        fields = ('fonction', 'diplome',)
        
class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'revue', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
class TheseForm(PublicationForm):
    titre = forms.CharField(required=True, label="Titre de la thèse ou du mémoire")
    annee = forms.IntegerField(required=False, label="Année de soutenance")
    editeur = forms.CharField(required=False, label="Directeur de thèse")
    lieu_edition = forms.CharField(required=False, label="Établissement de soutenance")
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
        

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('etablissement',)

class EtablissementAutreForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('etablissement_autre_nom', 'etablissement_autre_pays', )

class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('discipline', 'expertise', 'mots_cles', 'url_site_web', 'url_blog', 'url_facebook', 'url_linkedin')
        
class PersonneEditForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ('nom', 'prenom', 'genre') 
        
        
class RepertoireSearchForm (forms.Form):
    mots_cles = forms.CharField (required = False, label="Mots-clés")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Tous")
    domaine = forms.ModelChoiceField(queryset=Groupe.objects.all(), required=False, label="Domaine de recherche", empty_label="Tous")
    fonction = forms.ChoiceField(choices=(('','Tous'),)+FONCTION_CHOICES, required=False, label="Fonction")
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

