# -*- encoding: utf-8 -*-
import hashlib
from django import forms
from django.db.models import Q
from django.forms.models import inlineformset_factory
from itertools import chain
from models import *

OUI_NON_CHOICES = (('1', 'Oui'), ('0', 'Non'))

class PersonneForm(forms.ModelForm):
    genre = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENRE_CHOICES)

    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'courriel', 'genre')
        
    def clean_courriel(self):
        """On veut s'assurer qu'il n'y ait pas d'autre utilisateur actif
           avec le même courriel."""
        courriel = self.cleaned_data['courriel']
        existing = Personne.objects.filter(courriel=courriel, actif=True)
        if self.instance and self.instance.id:
            existing = existing.exclude(id=self.instance.id)
        if existing.count():
            raise forms.ValidationError('Il existe déjà une fiche pour cette adresse électronique')
        return courriel
        
class PersonneInscriptionForm(PersonneForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe") 
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label="Confirmez votre mot de passe")

    class Meta(PersonneForm.Meta):
        fields = ('nom', 'prenom', 'courriel', 'password', 'password_confirmation', 'genre')
        
    def clean_password_confirmation(self):
        """S'assurer que le mot de passe et la confirmation sont identiques."""
        password = self.cleaned_data.get('password')
        confirmation = self.cleaned_data.get('password_confirmation')
        if password != confirmation:
            raise forms.ValidationError('Les deux mots de passe ne correspondent pas.')
        return confirmation

    def save(self):
        self.instance.set_password(self.cleaned_data['password'])
        return super(PersonneInscriptionForm, self).save()

class ChercheurForm(forms.ModelForm):
    """Formulaire d'édition d'un chercheur."""
    ETABLISSEMENT_CHOICES = ((id, nom if len(nom) < 80 else nom[:80] + '...')
                             for id, nom in Etablissement.objects.filter(membre=True).values_list('id', 'nom'))

    membre_instance_auf = forms.ChoiceField(
        label="Êtes-vous (ou avez-vous déjà été) membre d'une instance de l'AUF?",
        help_text="e.g. conseil scientifique, conseil associatif, commission régionale d'experts",
        choices=OUI_NON_CHOICES, widget=forms.RadioSelect()
    )
    membre_instance_auf_details = forms.CharField(label="Préciser laquelle et votre fonction", required=False)
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
        label="Avez-vous fait partie des instances d'un réseau institutionnel de l'AUF?",
        help_text="e.g. AFELSH, RIFFEF, CIDMEF, etc.",
        choices=OUI_NON_CHOICES, widget=forms.RadioSelect()
    )
    membre_reseau_institutionnel_details = forms.CharField(required=False, label="Préciser lesquelles et votre fonction")
    membre_reseau_institutionnel_dates = forms.CharField(required=False, label="Préciser les dates")

    etablissement = forms.ChoiceField(label='Etablissement', required=False, choices=chain([('', '---------')], ETABLISSEMENT_CHOICES))

    class Meta:
        model = Chercheur
        fields = ('statut', 'diplome', 'etablissement',
                  'etablissement_autre_nom', 'etablissement_autre_pays',
                  'discipline', 'theme_recherche', 'groupe_recherche', 'mots_cles',
                  'url_site_web', 'url_blog', 'url_reseau_social',
                  'membre_instance_auf', 'membre_instance_auf_details', 'membre_instance_auf_dates',
                  'expert_oif', 'expert_oif_details', 'expert_oif_dates',
                  'membre_association_francophone',
                  'membre_association_francophone_details',
                  'membre_reseau_institutionnel', 'membre_reseau_institutionnel_details',
                  'membre_reseau_institutionnel_dates')
        
    def clean_membre_instance_auf(self):
        return bool(int(self.cleaned_data['membre_instance_auf']))
    
    def clean_membre_instance_auf_details(self):
        membre = self.cleaned_data.get('membre_instance_auf')
        details = self.cleaned_data.get('membre_instance_auf_details')
        if membre and not details:
            raise forms.ValidationError('Veuillez préciser')
        return details

    def clean_membre_instance_auf_dates(self):
        membre = self.cleaned_data.get('membre_instance_auf')
        dates = self.cleaned_data.get('membre_instance_auf_dates')
        if membre and not dates:
            raise forms.ValidationError('Veuillez préciser les dates')
        return dates

    def clean_expert_oif(self):
        return bool(int(self.cleaned_data['expert_oif']))

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
        return bool(int(self.cleaned_data['membre_association_francophone']))

    def clean_membre_association_francophone_details(self):
        membre = self.cleaned_data.get('membre_association_francophone')
        details = self.cleaned_data.get('membre_association_francophone_details')
        if membre and not details:
            raise forms.ValidationError('Veuillez préciser')
        return details
        
    def clean_membre_reseau_institutionnel(self):
        return bool(int(self.cleaned_data['membre_reseau_institutionnel']))

    def clean_membre_reseau_institutionnel_details(self):
        membre = self.cleaned_data.get('membre_reseau_institutionnel')
        details = self.cleaned_data.get('membre_reseau_institutionnel_details')
        if membre and not details:
            raise forms.ValidationError('Veuillez préciser')
        return details

    def clean_membre_reseau_institutionnel_dates(self):
        membre = self.cleaned_data.get('membre_reseau_institutionnel')
        dates = self.cleaned_data.get('membre_reseau_institutionnel_dates')
        if membre and not dates:
            raise forms.ValidationError('Veuillez préciser les dates')
        return dates

    def clean_etablissement(self):
        etablissement = self.cleaned_data['etablissement']
        if etablissement:
            return Etablissement.objects.get(id=etablissement)

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

class ChercheurInscriptionForm(ChercheurForm):
    attestation = forms.BooleanField(
        required=True, 
        label="J'atteste sur l'honneur l'exactitude des renseignements fournis sur le formulaire d'inscription et j'accepte leur publication en ligne."
    )

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
        fields = ('auteurs', 'titre', 'revue', 'annee', 'editeur', 'lieu_edition', 'nb_pages', 'url', 'publication_affichage')
        
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
    class Meta:
        model = Expertise
        fields = ('nom', 'date', 'organisme_demandeur', 'organisme_demandeur_visible')        

    def clean_organisme_demandeur_visible(self):
        value = self.cleaned_data['organisme_demandeur_visible']
        return bool(int(value)) if value else False

ExpertiseFormSet = inlineformset_factory(Chercheur, Expertise, form=ExpertiseForm, extra=1)

class ChercheurFormGroup(object):
    """Groupe de formulaires nécessaires pour l'inscription et l'édition
       d'un chercheur."""

    def __init__(self, data=None, chercheur=None):
        personne_form_class = PersonneInscriptionForm if chercheur is None else PersonneForm
        chercheur_form_class = ChercheurInscriptionForm if chercheur is None else ChercheurForm
        self.chercheur = chercheur_form_class(data=data, prefix='chercheur', instance=chercheur)
        self.groupes = GroupesForm(data=data, prefix='chercheur', chercheur=chercheur)
        self.personne = personne_form_class(data=data, prefix='personne', instance=chercheur and chercheur.personne.utilisateur)
        self.expertises = ExpertiseFormSet(data=data, prefix='expertise', instance=chercheur)
        self.these = TheseForm(data=data, prefix='these', instance=chercheur and chercheur.these)
        self.publications = PublicationFormSet(data=data, prefix='publication', instance=chercheur)

    @property
    def has_errors(self):
        return bool(self.chercheur.errors or self.personne.errors or self.groupes.errors or
                    self.these.errors or self.publications.errors or self.expertises.errors)

    def is_valid(self):
        return self.chercheur.is_valid() and self.personne.is_valid() and self.groupes.is_valid() and \
               self.these.is_valid() and self.publications.is_valid() and self.expertises.is_valid()

    def save(self):
        if self.is_valid():

            chercheur = self.chercheur.instance

            # Enregistrer d'abord les clés étrangères car on doit les stocker dans
            # l'objet chercheur.
            chercheur.personne = self.personne.save()

            # Puis enregistrer le chercheur lui-même.
            self.chercheur.save()

            # Puis les objets qui ont des clés étrangères vers nous
            # puisqu'on a besoin d'un id.
            self.groupes.chercheur = chercheur
            self.groupes.save()
            self.these.instance.chercheur = chercheur
            self.these.save()
            self.publications.instance = chercheur
            self.publications.save()
            self.expertises.instance = chercheur
            self.expertises.save()

class RepertoireSearchForm (forms.Form):
    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    nom = forms.CharField(required=False, label="Nom")
    domaine = forms.ModelChoiceField(queryset=Groupe.objects.all(), required=False, label="Domaine de recherche", empty_label="Tous")
    groupe_recherche = forms.CharField(required=False, label="Groupe de recherche",
                                       help_text="ou Laboratoire, ou Groupement inter-universitaire")
    statut = forms.ChoiceField(choices=(('','Tous'),)+STATUT_CHOICES+(('expert','Expert'),), required=False, label="Statut")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    pays = forms.ModelChoiceField(queryset=Pays.objects.all(), required=False, label="Pays", empty_label="Tous")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes",
                                    help_text="La région est ici définie au sens, non strictement géographique, du Bureau régional de l'AUF de référence.")
    nord_sud = forms.ChoiceField(choices=(('', 'Tous'), ('Nord', 'Nord'), ('Sud', 'Sud')), required=False, label="Nord/Sud",
                                 help_text="Distinction d'ordre géopolitique et économique, non géographique, qui conditionne souvent l'attribution de soutiens par les agences internationales: on entend par Nord les pays les plus développés, par Sud les pays en voie de développement.")

    def __init__(self, data=None, region=None):
        super(RepertoireSearchForm, self).__init__(data)
        if region:
            pays = self.fields['pays']
            pays.queryset = pays.queryset.filter(region=region)

    def get_query_set(self):
        chercheurs = Chercheur.objects
        if self.is_valid():
            q = self.cleaned_data["q"]
            if q:
                chercheurs = chercheurs.search(q)
            nom = self.cleaned_data['nom']
            if nom:
                chercheurs = chercheurs.add_to_query('@(nom,prenom) ' + nom)
            groupe_recherche = self.cleaned_data['groupe_recherche']
            if groupe_recherche:
                chercheurs = chercheurs.add_to_query('@groupe_recherche ' + groupe_recherche)
            discipline = self.cleaned_data['discipline']
            if discipline:
                chercheurs = chercheurs.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                chercheurs = chercheurs.filter_region(region)
            statut = self.cleaned_data["statut"]
            if statut:
                if statut == "expert":
                    chercheurs = chercheurs.filter_expert()
                else:
                    chercheurs = chercheurs.filter_statut(statut)
            domaine = self.cleaned_data["domaine"]
            if domaine:
                chercheurs = chercheurs.filter_groupe(domaine)
            pays = self.cleaned_data["pays"]
            if pays:
                chercheurs = chercheurs.filter_pays(pays)
            nord_sud = self.cleaned_data['nord_sud']
            if nord_sud:
                chercheurs = chercheurs.filter_nord_sud(nord_sud)
        return chercheurs.all()
    
class SendPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label="Adresse électronique")
    def clean_email(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        if email:
            try:
                Utilisateur.objects.get(courriel=email, actif=True)
            except:
                raise forms.ValidationError("Cette adresse n'existe pas dans notre base de données.")       
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

