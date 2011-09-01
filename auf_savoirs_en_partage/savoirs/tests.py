# coding: utf-8

from django.test import TestCase

class PageLoadTest(TestCase):

    fixtures = ['tests.yaml']

    def check_status_200(self, path, data={}):
        response = self.client.get(path, data)
        self.assertEqual(response.status_code, 200)

    def test_accueil(self):
        self.check_status_200('/')
        self.check_status_200('/region/1/')
        self.check_status_200('/discipline/1/')
        self.check_status_200('/discipline/1/region/1/')

    def test_recherche(self):
        self.check_status_200('/recherche/', dict(q='francophonie'))
        self.check_status_200('/region/1/recherche/', dict(q=u'université'))
        self.check_status_200('/discipline/1/recherche/', dict(q='ours noir'))
        self.check_status_200('/discipline/1/region/1/recherche/', dict(q='orientations -australie'))

    def test_ressources(self):
        self.check_status_200('/ressources/')
        self.check_status_200('/ressources/', {
            'q': "recherche textuelle",
            'auteur': 'Un auteur',
            'titre': 'Un titre',
            'sujet': 'Un sujet',
            'publisher': "Jean l'éditeur",
            'discipline': 1,
            'region': 1
        })

    def test_ressource(self):
        self.check_status_200('/ressources/1/')

    def test_agenda(self):
        self.check_status_200('/agenda/')
        self.check_status_200('/agenda/', {
            'q': 'foo',
            'titre': 'bar',
            'type': 'Colloque',
            'date_min': '18/01/2001',
            'date_max': '20/01/2001',
            'discipline': 1,
            'region': 1
        })
        self.check_status_200('/agenda/evenements/utilisation/')
        self.check_status_200('/agenda/evenements/creer/')

    def test_evenement(self):
        self.check_status_200('/agenda/evenements/1/')
        
    def test_actualites(self):
        self.check_status_200('/actualites/')
        self.check_status_200('/actualites/', {
            'q': 'mots-clés',
            'date_min': '01/01/2011',
            'date_max': '31/12/2011',
            'discipline': 1,
            'region': 1
        })
        self.check_status_200('/rss/actualites/')

    def test_actualite(self):
        self.check_status_200('/actualites/1/')
        self.check_status_200('/actualites/2/')

    def test_appels(self):
        self.check_status_200('/appels/')
        self.check_status_200('/appels/', {
            'q': 'mots-clés',
            'date_min': '01/01/2011',
            'date_max': '31/12/2011',
            'discipline': 1,
            'region': 1
        })
        self.check_status_200('/rss/appels/')

    def test_chercheurs(self):
        self.check_status_200('/chercheurs/')
        self.check_status_200('/chercheurs/', {
            'q': 'texte texte',
            'nom_chercheur': 'Ted Kennedy',
            'domaine': 1,
            'equipe_recherche': 'Le groupe',
            'statut': 'expert',
            'discipline': 1,
            'pays': 'AO',
            'region': 1,
            'nord_sud': 'Nord',
            'activites_francophonie': 'instance_auf',
            'genre': 'm'
        })
        self.check_status_200('/chercheurs/', dict(tri='nom'))
        self.check_status_200('/chercheurs/', dict(tri='nom_desc'))
        self.check_status_200('/chercheurs/', dict(tri='etablissement'))
        self.check_status_200('/chercheurs/', dict(tri='etablissement_desc'))
        self.check_status_200('/chercheurs/', dict(tri='pays'))
        self.check_status_200('/chercheurs/', dict(tri='pays_desc'))

    def test_sites(self):
        self.check_status_200('/sites/')
        self.check_status_200('/sites/', {
            'q': 'recherche',
            'discipline': 1,
            'pays': 'AO',
            'region': 1
        })

    def test_sites_auf(self):
        self.check_status_200('/sites-auf/')

    def test_contact(self):
        self.check_status_200('/nous-contacter/')

    def test_legal(self):
        self.check_status_200('/legal/')

    def test_a_propos(self):
        self.check_status_200('/a-propos/')

    def test_aide(self):
        self.check_status_200('/aide/')

    def test_rss(self):
        for brique in ['chercheurs', 'ressources', 'actualites', 'appels', 'agenda', 'sites']:
            self.check_status_200('/rss/ressources/')
            self.check_status_200('/rss/ressources/', {'q': 'test'})
