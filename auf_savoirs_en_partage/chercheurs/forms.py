# -*- encoding: utf-8 -*-
import hashlib
from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.db.models import Q
from django.forms.models import inlineformset_factory
from itertools import chain
from models import *

OUI_NON_CHOICES = ((True, 'Oui'), (False, 'Non'))

class ChercheurForm(forms.ModelForm):
    """Formulaire d'édition d'un chercheur."""
    genre = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENRE_CHOICES)
    afficher_courriel = forms.ChoiceField(
        label="Afficher mon courriel publiquement sur ce site",
        choices=OUI_NON_CHOICES, widget=forms.RadioSelect()
    )
    membre_instance_auf = forms.ChoiceField(
        label="Êtes-vous (ou avez-vous déjà été) membre d'une instance de l'AUF?",
        choices=OUI_NON_CHOICES, widget=forms.RadioSelect()
    )
    membre_instance_auf_nom = forms.ChoiceField(
        choices = (('', '---------'),) + Chercheur.INSTANCE_AUF_CHOICES,
        label="Préciser laquelle", required=False
    )
    membre_instance_auf_fonction = forms.CharField(label="Préciser votre fonction", required=False)
    membre_instance_auf_dates = forms.CharField(label="Préciser les dates", required=False)
    expert_oif = forms.ChoiceField(label="Avez-vous déjà été sollicité par l'OIF?", choices=OUI_NON_CHOICES, widget=forms.RadioSelect())
    expert_oif_details = forms.CharField(label="Préciser à quel titre", required=False,
                                         help_text="Fonction dans l'organisation, participation à une étude ou à une action, etc.")
    expert_oif_dates = forms.CharField(label="Préciser les dates", required=False)
    membre_association_francophone = forms.ChoiceField(
        label="Êtes-vous membre d'une association ou d'une société savante francophone?",
        help_text="e.g. FIPF, Collège international de philosophie, AISLF, etc.",
        choices=OUI_NON_CHOICES, widget=forms.RadioSelect()
    )
    membre_association_francophone_details = forms.CharField(label="Préciser laquelle", required=False)
    membre_reseau_institutionnel = forms.ChoiceField(
        label="Êtes-vous (ou avez-vous déjà été) membre des instances d'un réseau institutionnel de l'AUF?",
        choices=OUI_NON_CHOICES, widget=forms.RadioSelect()
    )
    membre_reseau_institutionnel_nom = forms.ChoiceField(
        label="Préciser le réseau institutionnel",
        choices=(('', '---------'),) + Chercheur.RESEAU_INSTITUTIONNEL_CHOICES,
        required=False
    )
    membre_reseau_institutionnel_fonction = forms.CharField(required=False, label="Préciser votre fonction")
    membre_reseau_institutionnel_dates = forms.CharField(required=False, label="Préciser les dates")

    pays_etablissement = forms.ModelChoiceField(label="Pays de l'établissement", queryset=Pays.objects.all(), required=True)
    etablissement = forms.CharField(
        label="Nom de l'établissement", required=True,
        help_text="Après avoir sélectionné un pays, une liste d'établissement apparaît dès la saisie partielle du nom de l'établissement."
    )

    pas_de_sollicitation_expertises = forms.BooleanField(
        required=False,
        label="Je ne souhaite pas être sollicité par l'AUF pour des missions d'expertise"
    )

    theme_recherche = forms.CharField(
        max_length=1000, label='Thèmes de recherche', help_text='1000 signes maximum',
        error_messages=dict(max_length="Veuillez entrer au maximum %(limit_value)d signes (vous en avez entré %(show_value)d)."),
        widget=forms.Textarea()
    )
    attestation = forms.BooleanField(
        required=True,
        label="J'atteste sur l'honneur l'exactitude des renseignements fournis sur le formulaire d'inscription et j'accepte leur publication en ligne."
    )
    discipline = forms.ModelChoiceField(
        label="Discipline", required=True,
        queryset=Discipline.objects.all(),
        help_text="La liste des disciplines procède d'un choix fait par le conseil scientifique de l'AUF."
    )
    groupe_recherche = forms.CharField(
        max_length=255, label='Groupe de recherche', required=False,
        help_text="Indiquer l'appartenance à un groupe de recherche universitaire ou laboratoire ou groupement inter-universitaire"
    )
    url_site_web = forms.URLField(
        label='Adresse site Internet', required=False,
        help_text="Si vous le souhaitez, vous pouvez y indiquer le lien qui renvoie vers une page personnelle (sur le site de votre établissement par exemple) plus complète."
    )

    class Meta:
        model = Chercheur
        fields = ('nom', 'prenom', 'genre', 'afficher_courriel', 'adresse_postale', 'telephone', 
                  'statut', 'diplome',
                  'discipline', 'theme_recherche', 'groupe_recherche',
                  'mots_cles', 'url_site_web', 'url_blog',
                  'url_reseau_social', 'attestation', 'membre_instance_auf',
                  'membre_instance_auf_nom', 'membre_instance_auf_fonction',
                  'membre_instance_auf_dates', 'expert_oif',
                  'expert_oif_details', 'expert_oif_dates',
                  'membre_association_francophone',
                  'membre_association_francophone_details',
                  'membre_reseau_institutionnel',
                  'membre_reseau_institutionnel_nom',
                  'membre_reseau_institutionnel_fonction',
                  'membre_reseau_institutionnel_dates')
        
    def __init__(self, data=None, prefix=None, instance=None):
        if instance is not None:
            initial = {}
            if instance.etablissement:
                initial['etablissement'] = instance.etablissement.nom
                initial['pays_etablissement'] = instance.etablissement.pays_id
            else:
                initial['etablissement'] = instance.etablissement_autre_nom
                initial['pays_etablissement'] = instance.etablissement_autre_pays_id
            initial['pas_de_sollicitation_expertises'] = not instance.expertises_auf
        else:
            initial = None
        super(ChercheurForm, self).__init__(data=data, prefix=prefix, instance=instance, initial=initial)

    def save(self):
        nom_etablissement = self.cleaned_data['etablissement']
        pays_etablissement = self.cleaned_data['pays_etablissement']
        etablissements = Etablissement.objects.filter(nom=nom_etablissement, pays=pays_etablissement, actif=True)
        if etablissements.count() > 0:
            self.instance.etablissement = etablissements[0]
            self.instance.etablissement_autre = ''
            self.instance.etablissement_autre_pays = None
        else:
            self.instance.etablissement = None
            self.instance.etablissement_autre_nom = nom_etablissement
            self.instance.etablissement_autre_pays = pays_etablissement
        self.instance.expertises_auf = not self.cleaned_data['pas_de_sollicitation_expertises']
        super(ChercheurForm, self).save()

    def clean_courriel(self):
        """On veut s'assurer qu'il n'y ait pas d'autre utilisateur actif
           avec le même courriel."""
        courriel = self.cleaned_data['courriel']
        existing = Chercheur.objects.filter(courriel=courriel, actif=True)
        if self.instance and self.instance.id:
            existing = existing.exclude(id=self.instance.id)
        if existing.count():
            raise forms.ValidationError('Il existe déjà une fiche pour cette adresse électronique')
        return courriel

    def clean_afficher_courriel(self):
        return self.cleaned_data['afficher_courriel'] == 'True'
            
    def clean_membre_instance_auf(self):
        return self.cleaned_data['membre_instance_auf'] == 'True'
    
    def clean_membre_instance_auf_nom(self):
        membre = self.cleaned_data.get('membre_instance_auf')
        nom = self.cleaned_data.get('membre_instance_auf_nom')
        if membre and not nom:
            raise forms.ValidationError('Veuillez préciser')
        return nom

    def clean_membre_instance_auf_fonction(self):
        membre = self.cleaned_data.get('membre_instance_auf')
        fonction = self.cleaned_data.get('membre_instance_auf_fonction')
        if membre and not fonction:
            raise forms.ValidationError('Veuillez préciser')
        return fonction

    def clean_membre_instance_auf_dates(self):
        membre = self.cleaned_data.get('membre_instance_auf')
        dates = self.cleaned_data.get('membre_instance_auf_dates')
        if membre and not dates:
            raise forms.ValidationError('Veuillez préciser les dates')
        return dates

    def clean_expert_oif(self):
        return self.cleaned_data['expert_oif'] == 'True'

    def clean_expert_oif_details(self):
        expert = self.cleaned_data.get('expert_oif')
        details = self.cleaned_data.get('expert_oif_details')
        if expert and not details:
            raise forms.ValidationError('Veuillez préciser')
        return details

    def clean_expert_oif_dates(self):
        expert = self.cleaned_data.get('expert_oif')
        dates = self.cleaned_data.get('expert_oif_dates')
        if expert and not dates:
            raise forms.ValidationError('Veuillez préciser les dates')
        return dates

    def clean_membre_association_francophone(self):
        return self.cleaned_data['membre_association_francophone'] == 'True'

    def clean_membre_association_francophone_details(self):
        membre = self.cleaned_data.get('membre_association_francophone')
        details = self.cleaned_data.get('membre_association_francophone_details')
        if membre and not details:
            raise forms.ValidationError('Veuillez préciser')
        return details
        
    def clean_membre_reseau_institutionnel(self):
        return self.cleaned_data['membre_reseau_institutionnel'] == 'True'

    def clean_membre_reseau_institutionnel_nom(self):
        membre = self.cleaned_data.get('membre_reseau_institutionnel')
        nom = self.cleaned_data.get('membre_reseau_institutionnel_nom')
        if membre and not nom:
            raise forms.ValidationError('Veuillez préciser')
        return nom

    def clean_membre_reseau_institutionnel_fonction(self):
        membre = self.cleaned_data.get('membre_reseau_institutionnel')
        fonction = self.cleaned_data.get('membre_reseau_institutionnel_fonction')
        if membre and not fonction:
            raise forms.ValidationError('Veuillez préciser')
        return fonction

    def clean_membre_reseau_institutionnel_dates(self):
        membre = self.cleaned_data.get('membre_reseau_institutionnel')
        dates = self.cleaned_data.get('membre_reseau_institutionnel_dates')
        if membre and not dates:
            raise forms.ValidationError('Veuillez préciser les dates')
        return dates

class ChercheurInscriptionForm(ChercheurForm):

    class Meta(ChercheurForm.Meta):
        fields = ChercheurForm.Meta.fields + ('courriel',)

class GroupesForm(forms.Form):
    """Formulaire qui associe des domaines de recherche et groupe de chercheur à un chercheur."""
    domaines_recherche = forms.ModelMultipleChoiceField(
        queryset=Groupe.domaine_recherche_objects.all(),
        label='Domaines de recherche', required=False,
        help_text="Ce champ est proposé à titre d'indication complémentaire, mais il n'est pas obligatoire. Maintenez appuyé « Ctrl », ou « Commande (touche pomme) » sur un Mac, pour en sélectionner plusieurs."
    )

    groupes_chercheur = forms.ModelMultipleChoiceField(
        queryset=Groupe.groupe_chercheur_objects.all(),
        label='Groupes de chercheur', required=False,
        help_text="Ce champ est proposé à titre d'indication complémentaire, mais il n'est pas obligatoire. Maintenez appuyé « Ctrl », ou « Commande (touche pomme) » sur un Mac, pour en sélectionner plusieurs."
    )

    def __init__(self, data=None, prefix=None, chercheur=None):
        self.chercheur = chercheur
        initial = {}
        if chercheur:
            initial['domaines_recherche'] = chercheur.domaines_recherche.values_list('id', flat=True)
            initial['groupes_chercheur'] = chercheur.groupes_chercheur.values_list('id', flat=True)
        super(GroupesForm, self).__init__(data=data, prefix=prefix, initial=initial)

    def save(self):
        if self.is_valid():
            domaines_recherche = self.cleaned_data['domaines_recherche']
            ChercheurGroupe.objects.filter(chercheur=self.chercheur).exclude(groupe__groupe_chercheur=True).exclude(groupe__in=domaines_recherche).delete()
            for dr in domaines_recherche:
                cg, created = ChercheurGroupe.objects.get_or_create(chercheur=self.chercheur, groupe=dr)
                if created:
                    cg.actif = 1
                    cg.save()

            groupes_chercheur = self.cleaned_data['groupes_chercheur']
            ChercheurGroupe.objects.filter(chercheur=self.chercheur).exclude(groupe__groupe_chercheur=False).exclude(groupe__in=groupes_chercheur).delete()
            for gc in groupes_chercheur:
                cg, created = ChercheurGroupe.objects.get_or_create(chercheur=self.chercheur, groupe=gc)
                if created:
                    cg.actif = 0
                    cg.save()

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('auteurs', 'titre', 'revue', 'annee', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
PublicationFormSet = inlineformset_factory(Chercheur, Publication, form=PublicationForm, extra=1)

class TheseForm(forms.ModelForm):
    class Meta:
        model = These
        fields = ('titre', 'annee', 'directeur', 'etablissement', 'nb_pages', 'url')
        
class ExpertiseForm(forms.ModelForm):
    organisme_demandeur_visible = forms.ChoiceField(
        label="Voulez-vous que l'organisme demandeur soit visible sur votre fiche?",
        choices=OUI_NON_CHOICES, widget=forms.RadioSelect(), required=False
    )
    nom = forms.CharField(label="Objet de l'expertise", required=False)

    class Meta:
        model = Expertise
        fields = ('nom', 'date', 'organisme_demandeur', 'organisme_demandeur_visible')        

    def clean_organisme_demandeur_visible(self):
        value = self.cleaned_data['organisme_demandeur_visible']
        return value == 'True'

ExpertiseFormSet = inlineformset_factory(Chercheur, Expertise, form=ExpertiseForm, extra=1)

class ChercheurFormGroup(object):
    """Groupe de formulaires nécessaires pour l'inscription et l'édition
       d'un chercheur."""

    def __init__(self, data=None, chercheur=None):
        try:
            these = chercheur and chercheur.these
        except These.DoesNotExist:
            these = These()
        chercheur_form_class = ChercheurInscriptionForm if chercheur is None else ChercheurForm
        self.chercheur = chercheur_form_class(data=data, prefix='chercheur', instance=chercheur)
        self.groupes = GroupesForm(data=data, prefix='chercheur', chercheur=chercheur)
        self.expertises = ExpertiseFormSet(data=data, prefix='expertise', instance=chercheur)
        self.these = TheseForm(data=data, prefix='these', instance=these)
        self.publications = PublicationFormSet(data=data, prefix='publication', instance=chercheur)

    @property
    def has_errors(self):
        return bool(self.chercheur.errors or self.groupes.errors or
                    self.these.errors or self.publications.errors or
                    self.expertises.errors)

    def is_valid(self):
        return self.chercheur.is_valid() and self.groupes.is_valid() and \
               self.these.is_valid() and self.publications.is_valid() and \
               self.expertises.is_valid()

    def save(self):
        if self.is_valid():

            # Enregistrer d'abord le chercheur lui-même.
            self.chercheur.save()

            # Puis les objets qui ont des clés étrangères vers nous
            # puisqu'on a besoin d'un id.
            chercheur = self.chercheur.instance
            self.groupes.chercheur = chercheur
            self.groupes.save()
            self.these.instance.chercheur = chercheur
            self.these.save()
            self.publications.instance = chercheur
            self.publications.save()
            self.expertises.instance = chercheur
            for expertise in self.expertises.save(commit=False):
                if expertise.nom:
                    expertise.save()
                elif expertise.id:
                    expertise.delete()
            return self.chercheur.instance

class GroupeSearchForm(forms.ModelForm):
    """Formulaire de recherche pour les groupes."""

    class Meta:
        model = GroupeSearch
        fields = ['q']

class ChercheurSearchForm(forms.ModelForm):
    """Formulaire de recherche pour les chercheurs."""

    class Meta:
        model = ChercheurSearch
        fields = ['q', 'nom_chercheur', 'domaine', 'groupe_chercheur',
                  'groupe_recherche', 'statut', 'discipline', 'pays',
                  'region', 'nord_sud', 'activites_francophonie', 'genre']

class ChercheurSearchEditForm(ChercheurSearchForm):
    """Formulaire d'édition d'une recherche sauvegardée."""

    class Meta(ChercheurSearchForm.Meta):
        fields = ['nom', 'alerte_courriel'] + ChercheurSearchForm.Meta.fields

class SendPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label="Adresse électronique")
    def clean_email(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        if email:
            try:
                Personne.objects.get(courriel=email)
            except:
                raise forms.ValidationError("Cette adresse n'existe pas dans notre base de données.")       
        return email

class SetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Mot de passe") 
    password_repeat = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirmez votre mot de passe")

    def clean_password_repeat(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError("Les mots de passe ne concordent pas")
        return password_repeat   

class AuthenticationForm(DjangoAuthenticationForm):
    username = forms.CharField(label='Courriel')


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('chercheur', 'groupe')
