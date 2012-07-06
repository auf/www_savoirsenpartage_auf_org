# encoding: utf-8

from urllib import urlopen
from urlparse import urlsplit, urlunsplit

from BeautifulSoup import BeautifulSoup

from savoirs.lib.utils import meta_set

META_MAP = {
    'author': 'creator',
    'dc.title': 'title',
    'dc.description': 'description',
    'dc.type': 'type',
    'dc.format': 'format',
    'dc.identifier': 'identifier',
    'dc.language': 'language',
    'dc.creator': 'creator',
    'dc.contributor': 'contributor',
    'dc.date': 'issued',
}


def harvest(options):
    """
    Moisonneur pour les systèmes Lodel 0.9.
    """
    # Boucle sur toutes les pages du site
    base_url = urlsplit(options['url'])
    pending_urls = set([options['url']])
    seen_urls = set()
    nodes = {}
    while pending_urls:

        # Lecture du contenu de la page
        current_url = pending_urls.pop()
        seen_urls.add(current_url)
        f = urlopen(current_url)
        if f.info().gettype() != 'text/html':
            f.close()
            continue
        html = f.read()
        f.close()
        soup = BeautifulSoup(html)
        if not soup.head:
            continue

        # Recherche de métadonnées
        node = {}
        for meta in soup.head('meta'):
            name = meta.get('name')
            content = meta.get('content')
            if not (name and content):
                continue
            field = META_MAP.get(name.lower())
            if not field:
                continue

            # Heurisitique pour déterminer si on a du contenu mal encodé
            # (encodé en utf-8, mais transmis comme du latin-1)
            if u'Ã' in content:
                try:
                    content = content.encode('latin-1').decode('utf-8')
                except UnicodeDecodeError:
                    pass

            meta_set(node, field, content)
        if 'identifier' in node and 'title' in node:
            node['uri'] = node['identifier']
            nodes[node['identifier']] = node

        # Recherche de liens vers d'autres pages du site
        new_urls = (
            urlunsplit((base_url.scheme, base_url.netloc, path, query, ''))
            for scheme, netloc, path, query, fragment in (
                urlsplit(a['href'].encode('utf8'))
                for a in soup('a', href=True)
            )
            if scheme in ('', base_url.scheme)
            and netloc in ('', base_url.netloc)
        )
        for url in new_urls:
            if url not in pending_urls and url not in seen_urls:
                pending_urls.add(url)

    return nodes.values()
