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

    def test_ressource(self):
        self.check_status_200('/ressources/1/')

    def test_agenda(self):
        self.check_status_200('/agenda/')
        self.check_status_200('/agenda/evenements/utilisation/')
        self.check_status_200('/agenda/evenements/creer/')

    def test_evenement(self):
        self.check_status_200('/agenda/evenements/1/')
        
    def test_actualites(self):
        self.check_status_200('/actualites/')
        self.check_status_200('/rss/actualites/')

    def test_actualite(self):
        self.check_status_200('/actualites/1/')
        self.check_status_200('/actualites/2/')

    def test_appels(self):
        self.check_status_200('/appels/')
        self.check_status_200('/rss/appels/')

    def test_chercheurs(self):
        self.check_status_200('/chercheurs/')
        self.check_status_200('/chercheurs/', dict(tri='nom'))
        self.check_status_200('/chercheurs/', dict(tri='nom_desc'))
        self.check_status_200('/chercheurs/', dict(tri='etablissement'))
        self.check_status_200('/chercheurs/', dict(tri='etablissement_desc'))
        self.check_status_200('/chercheurs/', dict(tri='pays'))
        self.check_status_200('/chercheurs/', dict(tri='pays_desc'))

    def test_sites(self):
        self.check_status_200('/sites/')

    def test_sites_auf(self):
        self.check_status_200('/sites-auf/')

    def test_contact(self):
        self.check_status_200('/nous-contacter/')

    def test_legal(self):
        self.check_status_200('/legal/')

    def test_a_propos(self):
        self.check_status_200('/a-propos/')
