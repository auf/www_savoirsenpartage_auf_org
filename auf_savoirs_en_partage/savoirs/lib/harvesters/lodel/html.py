# -*- encoding: utf-8 -*-
import re
from itertools import chain
from lxml import etree
from savoirs.globals import *
from savoirs.lib.utils import meta_set, smart_str
from urllib import urlopen
from urlparse import urljoin

DC_MAP = {'DC.Title': [TITLE,],
          'DCTERMS.alternative': [ALT_TITLE,],
          'DC.Creator': [CREATOR,],
          'DC.Contributor': [CONTRIBUTOR,],
          'DC.Description': [DESCRIPTION,],
          'DCTERMS.abstract': [ABSTRACT,],
          'DC.Subject': [SUBJECT,],
          'DC.Publisher': [PUBLISHER,],
          'DCTERMS.issued': [DATE_ISSUED,],
          'DCTERMS.modified': [DATE_MODIFIED,],
          'DC.Type': [TYPE,],
          'DC.Format': [FORMAT,],
          'DC.Identifier': [URI,],
          #'DC.Source': [SOURCE,], # ignoré, source pointe vers la recine du site
          'DC.Language': [LANGUAGE,],
         }

def harvest(options):
    """Méthode de moissonage pour systèmes Lodel < 0.8. Lodel, avant la version 
    0.8 n'offre pas de système d'exportation de données, autre que la 
    présentation des information OAI (Dublin Core) dans les tags *meta* des 
    pages des articles. On n'a pas non plus de facon d'obtenir la liste des 
    items existant dans l'instance.

    La méthode adoptée est d'y aller en *brute-force*, on cherche tout ce qui a 
    un *id* entre 0 et 100000, et on s'arrete si on a 200 erreurs consécutives.

    *options*
       *options* est un dictionnaire, et doit contenir au moins les attributs 
       suivants:

       *url*
          Racine de l'instance de Lodel.

    La méthode retourne une liste d'éléments correspondant au format de 
    metadonnées.
    """
    BASE_URL = options['url']

    def get_page(path):
        try:
            url = urljoin(BASE_URL, path)
            print "Récupération de la page:", url
            f = urlopen(url)
            page = f.read()
            f.close()
            return page
        except:
            print "Erreur: impossible de récupérer la page:", url
            return ''

    SOMMAIRE_ID_RE = re.compile(r'sommaire\.php\?id=(\d+)')
    def get_sommaire_ids(path):
        return SOMMAIRE_ID_RE.findall(get_page(path))

    AUTEUR_ID_RE = re.compile(r'personne\.php\?id=(\d+)')
    def get_auteur_ids(path):
        return AUTEUR_ID_RE.findall(get_page(path))

    ENTREE_TYPE_RE = re.compile(r'entrees\.php\?type=(\w+)')
    def get_entree_types(path):
        return ENTREE_TYPE_RE.findall(get_page(path))

    ENTREE_ID_RE = re.compile(r'entree\.php\?id=(\d+)')
    def get_entree_ids(path):
        return ENTREE_ID_RE.findall(get_page(path))

    DOCUMENT_ID_RE = re.compile(r'document\.php\?id=(\d+)')
    def get_document_ids(path):
        return DOCUMENT_ID_RE.findall(get_page(path))
    
    def get_meta(path):
        page = get_page(path)
        if not page:
            return None
        tree = etree.HTML(page)
        meta = { IDENTIFIER: urljoin(BASE_URL, path) }
        fields = tree.findall(".//meta")
        for field in fields:
            if field.attrib.get('lang', 'fr') == 'fr': # ignore en
                match = DC_MAP.get(field.attrib.get('name'))
                if match is not None:
                    for k in match:
                        meta_set(meta, k, smart_str(field.attrib.get('content')))
        if meta.get("uri") is not None:
            return meta

    nodes = []
    sommaire_ids = set(chain(get_sommaire_ids('/'), get_sommaire_ids('/index.php?format=numero')))
    auteur_ids = get_auteur_ids('/personnes.php?type=auteur')

    entree_types = get_entree_types('/')
    entree_ids = set()
    for type in entree_types:
        entree_ids.update(get_entree_ids('/entrees.php?type=%s' % type))

    document_ids = set()
    for id in sommaire_ids:
        path = '/sommaire.php?id=%s' % id
        meta = get_meta(path)
        if meta:
            nodes.append(meta)
        document_ids.update(get_document_ids(path))
    for id in auteur_ids:
        document_ids.update(get_document_ids('/personne.php?id=%s&type=auteur' % id))
    for id in entree_ids:
        document_ids.update(get_document_ids('/entree.php?id=%s' % id))

    for id in document_ids:
        meta = get_meta('/document.php?id=%s' % id)
        if meta:
            nodes.append(meta)
    return nodes
