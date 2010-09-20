# -*- encoding: utf-8 -*-
import sys
from lxml import etree
from urlparse import urlparse, urljoin
import sys, urllib, httplib, re, chardet

from auf_savoirs_en_partage.savoirs.models import ListSet
from auf_savoirs_en_partage.savoirs.globals import *
from auf_savoirs_en_partage.savoirs.lib.utils \
        import safe_append, print_structure, meta_set


map = {'title': [TITLE,],
       'creator': [CREATOR,],
       'contributor': [CONTRIBUTOR,],
       'subject': [SUBJECT,],
       'description': [DESCRIPTION,],
       'publisher': [PUBLISHER,],
       'date': [DATE_CREATION,],
       'type': [TYPE,],
       'identifier': [IDENTIFIER, URI],
       'format': [FORMAT,],
       'relation': [SOURCE,],
       }


def connect(url):
    handle = None 
    if url.scheme == 'https':
        port = 443
        if url.port is not None:
            port = url.port
        handle = httplib.HTTPSConnection (url.hostname, port)
    else:
        port = 80
        if url.port is not None:
            port = url.port
        handle = httplib.HTTPConnection (url.hostname, port)
    return handle

def find_location (url_str):
    url = urlparse(url_str)

    possible = ("perl/oai2", "cgi/oai2", "cgi-bin/oaiserver", "oai/oai.php", "oai/oai2.php")
    for test in possible:
        path = url.path + test
        handle = connect(url)
        handle.request ("GET", path + "?verb=Identify")
        r = handle.getresponse ()
        if r.status == 200:
            url = urlparse(urljoin(url.geturl(), test))
            break

    return url

def load_xml (url):
    ud = urllib.urlopen (url)
    original = ud.read()
    ud.close ()
    
    encoding = chardet.detect(original)['encoding']
    content = original.decode(encoding)

    # Greenstone crap
    content = content.replace ("\"http://www.openarchives.com/OAI/2.0\"",
                               "\"http://www.openarchives.org/OAI/2.0/\"")

    pattern = re.compile(r"<([/:\w]+)[>\s]", re.I|re.U)
    content = pattern.sub(lambda m: m.group(0).lower(), content)

    # Other crap
    content.replace("&", "&amp;")
    
    try:
        return etree.XML (content.encode("utf-8"))
    except:
        print "Erreur parser"
        print original
        sys.exit()

def store_listsets(options):
    """interroge le serveur pour récupérer tous les listsets et les stocke en bd."""

    oai2ns = "{http://www.openarchives.org/OAI/2.0/}"
    url = find_location (options['url'])
    root = load_xml (url.geturl() + "?verb=ListSets")
    sets = root.findall (".//%sset" % oai2ns)
    
    listsets = [{'spec':e[0].text , 'name':e[1].text, 'server':options['server']} for e in sets]
    for data in listsets:
        ls, created = ListSet.objects.get_or_create(spec = data['spec'])
        del data['spec']
        for k,v in data.items():
            setattr(ls, k, v)
        ls.save()


def harvest (options):
    """Méthode de moissonage générique pour un système capable d'exporter ses 
    données au format `OAI <http://www.openarchives.org/>`_.

    *options*
       *options* est un dictionnaire, et doit contenir au moins les attributs 
       suivants:

       *server*
          Nom du serveur distant.
       *port*
          Port du service http.
       *base_url*
          Racine de l'acces OAI.

    La méthode retourne une liste d'éléments correspondant au format de 
    metadonnées.
    """
    oai2ns = "{http://www.openarchives.org/OAI/2.0/}"
    oaidc  = "{http://www.openarchives.org/OAI/2.0/oai_dc/}dc"
    metans = "{http://purl.org/dc/elements/1.1/}"

    # récupère les listsets du serveur
    store_listsets(options)

    url = find_location (options['url'])

    records = []
    root = load_xml (url.geturl() + "?verb=ListRecords&metadataPrefix=oai_dc")
    records.extend (root.findall (".//%srecord" % oai2ns))
    token = root.find (".//%sresumptiontoken" % oai2ns)
    print "total du serveur %s " % token.get("completeListSize")

    while token is not None:
        root = load_xml (url.geturl() + "?verb=ListRecords&resumptionToken=%s" % token.text)
        records.extend (root.findall (".//%srecord" % oai2ns))
        token = root.find (".//%sresumptiontoken" % oai2ns)


    nodes = []
    for record in records:
        meta = {}
        node = record.find (".//%sheader/%sdatestamp" % (oai2ns, oai2ns))

        meta[DATE_MODIFIED] = node.text

        dcnode = record.find (".//%s" % oaidc)
        if dcnode is not None:
            for c in dcnode.getchildren ():
                if c.text:
                    c.text = c.text.strip ()
                else:
                    c.text = ""
    
                if len (c.text) > 0:
                    match = map.get (c.tag.replace (metans, ""), [])
                    if c.tag.replace(metans, "") == "identifier" \
                       and not c.text.startswith("http"):
                        pass
                    else:
                        for field in match:
                            meta_set (meta, field, c.text)

            #print meta, etree.tostring(record, pretty_print = True)
            if meta.get("uri") is None and meta.get("source") is not None:
                meta['uri'] = meta['source']

            # récupère les listsets associés
            listsets = record.findall (".//%sheader/%ssetspec" % (oai2ns, oai2ns))
            meta['listsets'] = [l.text for l in listsets]

            if meta.get("uri") is not None:
                nodes.append (meta)
    print "total récupérés %s" % len(nodes)       
    return nodes
