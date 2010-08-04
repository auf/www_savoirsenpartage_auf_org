# -*- encoding: utf-8 -*-
from pmbclient import PmbClient
from lxml import etree
import sys, re

from auf_savoirs_en_partage_backend.globals import *
from auf_savoirs_en_partage_backend.sep.utils import print_structure, find_text, meta_set


def read_person (node):
    rc = u"%s %s" % (find_text(node, "prenom"), 
            find_text(node, "nom"))
    dates = find_text(node, "dates")
    if len (dates) > 0:
        rc += " (%s)" % dates
    return rc

def read_publisher (node):
    return u"%s, %s" % (find_text(node, "nom"), 
            find_text(node, "ville"))
    


def harvest (options):
    """Méthode de moissonage pour PMB utilisant la fonction d'export de 
    l'interface admin.

    *options*
       *options* est un dictionnaire, et doit contenir au moins les attributs 
       suivants:

       *host*
          Nom du serveur distant.
       *base_url*
          Racine de l'acces OAI.
       *user*
          Nom d'utilisateur ayant droit d'accès a l'admin
       *password*
          Mot de passe de l'utilisateur
       *database*
          Nom de la base de données que PMB utilise

    """
    c = PmbClient ()
    c.connect (options['host'])
    login_script = options['base_url'] + "main.php"
    export_script = options['base_url'] + "admin/convert/start_export.php"

    params = {'user': options['username'], 
            'password': options['password'], 
            'database': options['db']}
    c.login (params, login_script)

    params = {'export_type': '14', 'lender': 'x'}
    content = c.export (params, export_script)

    root = etree.XML (content.encode("utf-8"))
    article_nodes = root.findall (".//notice")
    nodes = []
    for node in article_nodes:
        meta = {}
        for c in node.getchildren ():
            if c.text:
                c.text = c.text.strip ()

            if c.tag == 'idNotice':
                meta_set (meta, IDENTIFIER, c.text)

            elif c.tag == 'zoneTitre':
                for t in c.getchildren ():
                    if t.tag == 'titrePrincipal':
                        meta_set (meta, TITLE, t.text)
                    else:
                        meta_set (meta, ALT_TITLE, t.text)

            elif c.tag == 'zoneAuteurPrincipal':
                meta_set (meta, CREATOR, read_person (c))

            elif c.tag == 'zoneAuteursAutres':
                meta_set (meta, CONTRIBUTOR, read_person (c))

            elif c.tag == 'zoneNotes':
                meta_set (meta, ABSTRACT, find_text (c, "noteResume"))

            elif c.tag == 'zoneEditeur':
                meta_set (meta, PUBLISHER, read_publisher (c))
                meta_set (meta, DATE_ISSUED, find_text (c, "annee"))

            elif c.tag == 'prixISBN':
                meta_set (meta, ISBN, find_text (c, "ISBN"))

            elif c.tag == 'zoneLiens':
                meta_set (meta, SOURCE, find_text (c, "lien"))

            elif c.tag == 'zoneLangue':
                for t in c.getchildren ():
                    if t.tag == 'langueDocument':
                        meta_set (meta, LANGUAGE, t.text)
                    elif t.tag == 'langueOriginale':
                        meta_set (meta, ORIG_LANG, t.text)

            elif c.tag == 'zoneCategories':
                meta_set (meta, SUBJECT, find_text (c, "categorie"))

        meta_set (meta, URI, "http://%s%scatalog.php?id=%s" % \
                (options['host'], options['base_url'], meta[IDENTIFIER]))

        nodes.append (meta)
    return nodes


