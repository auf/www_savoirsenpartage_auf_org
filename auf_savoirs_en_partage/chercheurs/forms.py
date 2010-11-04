# -*- encoding: utf-8 -*-
import hashlib
from django import forms
from django.db.models import Q
from models import *

class PersonneForm(forms.ModelForm):
    genre = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENRE_CHOICES)

    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'courriel', 'genre')
        
class PersonneInscriptionForm(PersonneForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe") 

    class Meta(PersonneForm.Meta):
        fields = ('nom', 'prenom', 'courriel', 'password', 'genre')
        
    def clean_password(self):
        """Encrypter le mot de passe avant de le mettre dans la BD."""
        return hashlib.md5(self.cleaned_data['password']).hexdigest()

class ChercheurForm(forms.ModelForm):
    """Formulaire d'édition d'un chercheur."""
    OUI_NON_CHOICES = ((1, 'Oui'), (0, 'Non'))

    membre_instance_auf = forms.ChoiceField(
        choices=OUI_NON_CHOICES, 
        label="Êtes-vous (ou avez-vous déjà été) membre d'une instance de l'AUF?",
        help_text="e.g. conseil scientifique, conseil associatif, commission régionale d'experts",
        widget=forms.RadioSelect()
    )
    membre_instance_auf_dates = forms.CharField(label="Préciser les dates", required=False)
    expert_oif = forms.ChoiceField(choices=OUI_NON_CHOICES,
                                   label="Êtes-vous expert de l'OIF?",
                                   widget=forms.RadioSelect())
    membre_fipf = forms.ChoiceField(choices=OUI_NON_CHOICES,
                                    label="Êtes-vous membre de la FIPF?",
                                    widget=forms.RadioSelect())
    membre_fipf_association = forms.CharField(label="Préciser le nom de votre association", required=False)

    class Meta:
        model = Chercheur
        fields = ('statut', 'diplome', 'etablissement',
                  'etablissement_autre_nom', 'etablissement_autre_pays',
                  'discipline', 'theme_recherche', 'groupe_recherche', 'mots_cles',
                  'url_site_web', 'url_blog', 'url_reseau_social',
                  'membre_instance_auf', 'membre_instance_auf_dates',
                  'expert_oif', 'membre_fipf', 'membre_fipf_association')
        
    def clean(self):
        etablissement = self.cleaned_data['etablissement']
        etablissement_autre_nom = self.cleaned_data['etablissement_autre_nom']
        etablissement_autre_pays = self.cleaned_data['etablissement_autre_pays']
        if not etablissement:
            if not etablissement_autre_nom:
                self._errors['etablissement'] = self.error_class([u"Vous devez renseigner l'établissement"])
            elif not etablissement_autre_pays:
                self._errors['etablissement_autre_pays'] = self.error_class([u"Vous devez renseigner le pays de l'établissement"])
        return self.cleaned_data

    def clean_membre_instance_auf(self):
        """Transforme la valeur du champ en booléen"""
        return bool(int(self.cleaned_data['membre_instance_auf']))

    def clean_expert_oif(self):
        """Transforme la valeur du champ en booléen"""
        return bool(int(self.cleaned_data['expert_oif']))

    def clean_membre_fipf(self):
        """Transforme la valeur du champ en booléen"""
        return bool(int(self.cleaned_data['membre_fipf']))

class GroupesForm(forms.Form):
    """Formulaire qui associe des groupes à un chercheur."""
    groupes = forms.ModelMultipleChoiceField(
        queryset=Groupe.objects.all(), 
        label='Domaines de recherche', required=False,
        help_text="Maintenez appuyé « Ctrl », ou « Commande (touche pomme) » sur un Mac, pour en sélectionner plusieurs."
    )

    def __init__(self, data=None, prefix=None, chercheur=None):
        self.chercheur = chercheur
        initial = {}
        if chercheur:
            initial['groupes'] = chercheur.groupes.values_list('id', flat=True)
        super(GroupesForm, self).__init__(data=data, prefix=prefix, initial=initial)

    def save(self):
        if self.is_valid():
            groupes = self.cleaned_data['groupes']
            ChercheurGroupe.objects.filter(chercheur=self.chercheur).exclude(groupe__in=groupes).delete()
            for g in groupes:
                ChercheurGroupe.objects.get_or_create(chercheur=self.chercheur, groupe=g, actif=1)

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'revue', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
class TheseForm(PublicationForm):
    titre = forms.CharField(required=True, label="Titre de la thèse ou du mémoire")
    annee = forms.IntegerField(required=True, label="Année de soutenance (réalisée ou prévue)")
    editeur = forms.CharField(required=True, label="Directeur de thèse")
    lieu_edition = forms.CharField(required=True, label="Établissement de soutenance")
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
class ExpertiseForm(forms.ModelForm):
    class Meta:
        model = Expertise
        fields = ('nom', 'date', 'organisme_demandeur', 'organisme_demandeur_visible')        

class ChercheurFormGroup(object):
    """Groupe de formulaires nécessaires pour l'inscription et l'édition
       d'un chercheur."""

    def __init__(self, data=None, chercheur=None):
        personne_form_class = PersonneInscriptionForm if chercheur is None else PersonneForm
        self.chercheur = ChercheurForm(data=data, prefix='chercheur', instance=chercheur)
        self.groupes = GroupesForm(data=data, prefix='chercheur', chercheur=chercheur)
        self.personne = personne_form_class(data=data, prefix='personne', instance=chercheur and chercheur.personne)
        self.publication1 = PublicationForm(data=data, prefix='publication1', instance=chercheur and chercheur.publication1)
        self.publication2 = PublicationForm(data=data, prefix='publication2', instance=chercheur and chercheur.publication2)
        self.publication3 = PublicationForm(data=data, prefix='publication3', instance=chercheur and chercheur.publication3)
        self.publication4 = PublicationForm(data=data, prefix='publication4', instance=chercheur and chercheur.publication4)
        self.these = TheseForm(data=data, prefix='these', instance=chercheur and chercheur.these)
        self.expertise = ExpertiseForm(data=data, prefix='expertise', instance=chercheur and chercheur.expertise)

    @property
    def has_errors(self):
        return bool(self.chercheur.errors or self.personne.errors or self.groupes.errors or
                    self.publication1.errors or self.publication2.errors or self.publication3.errors or
                    self.publication4.errors or self.these.errors or self.expertise.errors)

    def is_valid(self):
        return self.chercheur.is_valid() and self.personne.is_valid() and self.groupes.is_valid() and \
               self.publication1.is_valid() and self.publication2.is_valid() and \
               self.publication3.is_valid() and self.publication4.is_valid() and \
               self.these.is_valid() and self.expertise.is_valid()

    def save(self):
        if self.is_valid():

            chercheur = self.chercheur.instance

            # Enregistrer d'abord les clés étrangères car on doit les stocker dans
            # l'objet chercheur.
            chercheur.personne = self.personne.save()
            if self.publication1.cleaned_data['titre']:
                chercheur.publication1 = self.publication1.save()
            if self.publication2.cleaned_data['titre']:
                chercheur.publication2 = self.publication2.save()
            if self.publication3.cleaned_data['titre']:
                chercheur.publication3 = self.publication3.save()
            if self.publication4.cleaned_data['titre']:
                chercheur.publication4 = self.publication4.save()
            chercheur.these = self.these.save()
            if self.expertise.cleaned_data['nom']:
                chercheur.expertise = self.expertise.save()

            # Puis enregistrer le chercheur lui-même.
            self.chercheur.save()

            # Puis les many-to-many puisqu'on a besoin d'un id.
            self.groupes.chercheur = chercheur
            self.groupes.save()

class RepertoireSearchForm (forms.Form):
    mots_cles = forms.CharField(required=False, label="Rechercher dans tous les champs")
    nom = forms.CharField(required=False, label="Nom")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Tous")
    domaine = forms.ModelChoiceField(queryset=Groupe.objects.all(), required=False, label="Domaine de recherche", empty_label="Tous")
    statut = forms.ChoiceField(choices=(('','Tous'),)+STATUT_CHOICES+(('expert','Expert'),), required=False, label="Statut")
    pays = forms.ModelChoiceField(queryset=Pays.objects.all(), required=False, label="Pays", empty_label="Tous")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes")
    nord_sud = forms.ChoiceField(choices=(('', 'Tous'), ('Nord', 'Nord'), ('Sud', 'Sud')), required=False, label="Nord/Sud")
      
    def get_query_set(self):
        qs = Chercheur.objects.all()
        if self.is_valid():
            nom = self.cleaned_data['nom']
            if nom:
                qs = qs.search_nom(nom)
            discipline = self.cleaned_data["discipline"]
            if discipline:
                qs = qs.filter(discipline=discipline)
            domaine = self.cleaned_data["domaine"]
            if domaine:
                qs = qs.filter(groupes=domaine)
            mots_cles = self.cleaned_data["mots_cles"]
            if mots_cles:
                qs = qs.search(mots_cles)
            statut = self.cleaned_data["statut"]
            if statut:
                if statut == "expert":
                    qs = qs.exclude(expertise=None)
                else:
                    qs = qs.filter(statut=statut)
            pays = self.cleaned_data["pays"]
            if pays:
                qs = qs.filter(Q(etablissement__pays=pays) | Q(etablissement_autre_pays=pays))
            region = self.cleaned_data['region']
            if region:
                qs = qs.filter(Q(etablissement__pays__region=region) | Q(etablissement_autre_pays__region=region))
            nord_sud = self.cleaned_data['nord_sud']
            if nord_sud:
                qs = qs.filter(Q(etablissement__pays__nord_sud=nord_sud) | Q(etablissement_autre_pays__nord_sud=nord_sud))
        return qs
    
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

