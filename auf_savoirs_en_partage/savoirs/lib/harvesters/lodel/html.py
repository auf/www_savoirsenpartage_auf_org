# -*- encoding: utf-8 -*-
from lxml import etree
import sys, httplib, re, pprint, simplejson
from urlparse import urlparse, urljoin

from auf_savoirs_en_partage.savoirs.globals import *
from auf_savoirs_en_partage.savoirs.lib.utils \
        import safe_append, print_structure, meta_set, smart_str


map = {'DC.Title': [TITLE,],
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


def load_html (host, base, id):
    root = None
    handle = httplib.HTTPConnection (host)
    uri = base + "document.php?id=%d" % id
    handle.request ("GET", uri)
    r = handle.getresponse ()
    if r.status == 302:
        del (handle)
        del (r)
        handle = httplib.HTTPConnection (host)
        uri = base + "sommaire.php?id=%d" % id
        handle.request ("GET", uri)
        r = handle.getresponse ()

    if r.status == 200:
        content = smart_str(r.read ())
        handle.close ()
        root = etree.HTML (content)

    return ("http://" + host + uri, root)


def harvest (options):
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
    url = urlparse(options['url'])


    ## BRUTE FORCE POWER!
    max_err = 5000
    err_count = 0
    
    nodes = []
    for i in range(0, 50000):
        (loc, root) = load_html (url.hostname, url.path, i)

        if root is not None:
            err_count = 0
            meta = {IDENTIFIER: loc}
            fields = root.findall (".//meta")
            for field in fields:
                if field.attrib.get('lang', 'fr') == 'fr': # ignore en
                    match = map.get (field.attrib.get('name'))
                    if match is not None:
                        for k in match:
                            meta_set (meta, k, smart_str(field.attrib.get('content')))

            if meta.get("uri") is not None:
                nodes.append (meta)
        else:
            err_count += 1

        if err_count >= max_err:
            print i, "erreurs:", err_count
            break


    return nodes
