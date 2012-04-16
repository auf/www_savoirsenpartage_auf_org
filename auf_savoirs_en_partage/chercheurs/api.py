# -*- encoding: utf-8 -*

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.utils import simplejson

from savoirs.rss import FilChercheurs
from auf.django.references import models as ref
from chercheurs.models import Chercheur
from chercheurs.forms import ChercheurSearchForm

STATUS_OK = 200
STATUS_ERROR = 400
STATUS_ERROR_PERMISSIONS = 403 
STATUS_ERROR_NOT_FOUND = 404
STATUS_ERROR_BADMETHOD = 405

def recherche(request):
    """
    API spéciale de recherche pour retourner une structure de données complète
    par rapport au RSS.
    """
    search_form = ChercheurSearchForm(request.GET)
    search = search_form.save(commit=False)
    data = []

    # S'assure qu'un filtre existe au moins
    no_criterion = True
    for criterion, val in request.GET.items():
        if val not in (None, u'', ''):
            no_criterion = False
            break
    if no_criterion:
        return api_return(STATUS_ERROR, 'no criterion', True)

    # run() de ChercheurSearchForm()
    results = Chercheur.objects
    if search.q:
        results = results.search(search.q)
    if search.nom_chercheur:
        results = results.add_to_query('@(nom,prenom) ' + search.nom_chercheur)
    if search.equipe_recherche:
        results = results.add_to_query('@equipe_recherche ' + search.equipe_recherche)
    if search.discipline:
        results = results.filter_discipline(search.discipline)
    if search.region:
        results = results.filter_region(search.region)
    if search.statut:
        if search.statut == "expert":
            results = results.filter_expert()
        else:
            results = results.filter_statut(search.statut)
    if search.domaine:
        results = results.filter_groupe(search.domaine)
    if search.pays:
        results = results.filter_pays(search.pays)
    if search.nord_sud:
        results = results.filter_nord_sud(search.nord_sud)
    if search.genre:
        results = results.filter_genre(search.genre)
    if search.activites_francophonie == 'instance_auf':
        results = results.filter(membre_instance_auf=True)
    elif search.activites_francophonie == 'expert_oif':
        results = results.filter(expert_oif=True)
    elif search.activites_francophonie == 'association_francophone':
        results = results.filter(membre_association_francophone=True)
    elif search.activites_francophonie == 'reseau_institutionnel':
        results = results.filter(membre_reseau_institutionnel=True)

    # sous-ensemble de pays
    limitation_pays = request.GET.get('limitation_pays', None)
    
    if limitation_pays is not None:
        pays = [ref.Pays.objects.get(code=pays_code) for pays_code in limitation_pays.split(',')]
        results = results.filter_pays(pays)

    for chercheur in results.all():
        data.append(chercheur_2_dict(chercheur))
    
    return api_return(STATUS_OK, dict_2_json(data), True)


def api(request, pays=None, region=None, chercheur_id=None):
    api = API(request)
    if chercheur_id is not None:
        return api.api_chercheur(chercheur_id)
    elif pays is not None:
        filter_pays = pays.split(',')
        return api.api_chercheurs_liste(pays=filter_pays)
    else:
        return api.api_chercheurs_liste(region=region)

def api_return(status, text='', json=False):
    content_type = 'text/html'
    if status == STATUS_OK and json:
        content_type = 'text/json'
    if text is None:
        if status == STATUS_ERROR:
            text = 'Error'
        elif status == STATUS_ERROR_NOT_FOUND:
            text = 'Resource Not Found'
        elif status == STATUS_ERROR_PERMISSIONS:
            text = 'Invalid username or password'
        elif status == STATUS_ERROR_BADMETHOD:
            text = 'Invalid request method'
        elif status == STATUS_OK:
            text = 'OK'

    r = HttpResponse(status=status, content=text, content_type=content_type)

    if status == STATUS_ERROR_BADMETHOD:
        r.Allow = 'POST'

    return r


def dict_2_json(data):
    return simplejson.dumps(data, indent=4)


def chercheur_2_dict(chercheur):
    """
    Structure flat d'un chercheur pour JSON
    """
    # Domaines de recherche du chercheur
    domaines_recherche = []
    for dr in chercheur.domaines_recherche:
        domaines_recherche.append(dr.nom)

    # Groupes chercheur
    groupes_chercheur = []
    for gc in chercheur.groupes_chercheur:
        groupes_chercheur.append(gc.nom)

    # Expertises
    expertises = []
    for exp in chercheur.expertises.all():
        expertises.append(
        {'nom': '%s' % exp.nom,
            'date': '%s' % exp.date,
            'organisme_demandeur': '%s' % exp.organisme_demandeur,
            'organisme_demandeur_visible': exp.organisme_demandeur_visible})

    # Publications
    publications = []
    for pub in chercheur.publications.all():
        publications.append(
        {'auteurs': '%s' % pub.auteurs,
            'titre': '%s' % pub.titre,
            'revue': '%s' % pub.revue,
            'annee': '%s' % pub.annee,
            'editeur': '%s' % pub.editeur,
            'lieu_edition': '%s' % pub.lieu_edition,
            'nb_pages': '%s' % pub.nb_pages,
            'url': '%s' % pub.url,
            'publication_affichage': '%s' %  pub.publication_affichage})

    chercheur_details = {'id': '%s' % chercheur.id, 
            'civilite': '%s' % chercheur.civilite, 
            'prenom': '%s' % chercheur.prenom, 
            'nom': '%s' % chercheur.nom,
            'pays': '%s' % chercheur.pays,
            'pays_code': '%s' % chercheur.pays.code,
            'etablissement': '%s' % chercheur.etablissement_display,
            'afficher_courriel': '%s' % chercheur.afficher_courriel,
            'courriel': '%s' % chercheur.courriel_display(), 
            'region': '%s' % chercheur.region.nom, 
            'statut': '%s' % chercheur.get_statut_display(), 
            'diplome': '%s' % chercheur.diplome, 
            'domaines_recherche': domaines_recherche,
            'discipline': '%s' % chercheur.discipline,
            'theme_recherche': '%s' % chercheur.theme_recherche, 
            'equipe_recherche': '%s' % chercheur.equipe_recherche, 
            'mots_cles': '%s' % chercheur.mots_cles, 
            'url_site_web': '%s' % chercheur.url_site_web, 
            'url_blog': '%s' % chercheur.url_blog, 
            'url_reseau_social': '%s' % chercheur.url_reseau_social, 
            'membre_instance_auf': chercheur.membre_instance_auf, 
            'expert_oif': chercheur.expert_oif, 
            'membre_association_francophone': chercheur.membre_association_francophone, 
            'membre_reseau_institutionnel': chercheur.membre_reseau_institutionnel, 
            'membre_instance_auf_nom': '%s' % chercheur.get_membre_instance_auf_nom_display(), 
            'membre_instance_auf_fonction': '%s' % chercheur.membre_instance_auf_fonction, 
            'membre_instance_auf_dates': '%s' % chercheur.membre_instance_auf_dates, 
            'expert_oif_details': '%s' % chercheur.expert_oif_details, 
            'expert_oif_dates': '%s' % chercheur.expert_oif_dates, 
            'membre_association_francophone_details': '%s' % chercheur.membre_association_francophone_details, 
            'membre_reseau_institutionnel_nom': '%s' %
            chercheur.get_membre_reseau_institutionnel_nom_display(), 
            "membre_reseau_institutionnel_fonction": "%s" % chercheur.membre_reseau_institutionnel_fonction, 
            "membre_reseau_institionnel_dates": "%s" % chercheur.membre_reseau_institutionnel_dates, 
            "expertises": expertises, 
            "expertises_auf": chercheur.expertises_auf,
            "publications": publications}

    # devrait faire le lookup 
    try:
        if chercheur.these:
            chercheur_details['these'] = {"these" : "%s" % chercheur.these,
                "these_url": "%s" % chercheur.these.url, 
                "these_titre": "%s" % chercheur.these.titre, 
                "these_etablissement": "%s" % chercheur.these.etablissement, 
                "these_annee": "%s" % chercheur.these.annee, 
                "these_nb_pages": "%s" % chercheur.these.nb_pages, 
                "these_directeur": "%s" % chercheur.these.directeur, 
                }
    except:
        pass
    return chercheur_details


class API:
    def __init__(self, request):
        self.request = request

    def api_chercheur(self, chercheur_id):
        chercheur = get_object_or_404(Chercheur, id=chercheur_id)
        chercheur_details = chercheur_2_dict(chercheur)
        return api_return(STATUS_OK, dict_2_json(chercheur_details), True)     
        

    def api_chercheurs_liste(self, pays=None, region=None):
        if pays is not None:
            chercheurs = Chercheur.objects.filter(etablissement__pays__in=pays) | Chercheur.objects.filter(etablissement_autre_pays__in=pays)
        elif region is not None:
            chercheurs = Chercheur.objects.filter_region(region)
        else:
            return api_return(STATUS_ERROR, "Erreur dans la requete de recherche de chercheurs")

        results = []
        for c in chercheurs:            
            if c.etablissement_autre_pays is not None:
                etablissement_autre_pays_nom = c.etablissement_autre_pays.nom
            else:
                etablissement_autre_pays_nom = None
            
            if c.etablissement is not None:
                    etablissement = c.etablissement.nom
            else:
                etablissement = c.etablissement_autre_nom

            data = {"id": "%s" % c.id,
                "nom": "%s" % c.nom,
                "prenom": "%s" % c.prenom,
                "etablissement": "%s" % etablissement,
                "etablissement_autre_nom": "%s" % c.etablissement_autre_nom,
                "pays": "%s" % c.pays.nom,
                "etablissement_pays_autre_nom": "%s" % etablissement_autre_pays_nom}
            results.append(data)

        return api_return(STATUS_OK, dict_2_json(results), json=True)

