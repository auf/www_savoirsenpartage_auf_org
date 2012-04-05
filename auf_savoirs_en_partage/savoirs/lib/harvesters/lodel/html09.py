# encoding: utf-8

from itertools import chain
from urllib import urlopen
from urlparse import urljoin

from BeautifulSoup import BeautifulSoup

from savoirs.lib.utils import meta_set

META_MAP = {
    'dc.title': 'title',
    'dc.description': 'description',
    'dc.type': 'type',
    'dc.format': 'format',
    'dc.identifier': 'uri',
    'dc.language': 'language',
    'dc.creator': 'creator',
    'dc.contributor': 'contributor',
    'dc.date': 'issued',
}


def harvest(options):
    """
    Moisonneur pour les systèmes Lodel 0.9.
    """

    BASE_URL = options['url']

    def get_soup(path):
        url = urljoin(BASE_URL, path)
        f = urlopen(url)
        html = f.read()
        f.close()
        return BeautifulSoup(html)

    def get_node(path):
        soup = get_soup(path)
        uri = urljoin(BASE_URL, path)
        node = {'identifier': uri, 'uri': uri}
        for meta in soup.head('meta'):
            name = meta.get('name')
            content = meta.get('content')
            if not (name and content):
                continue
            field = META_MAP.get(name.lower())
            if not field:
                continue
            meta_set(node, field, content)
        return node

    index_soup = get_soup('/')
    auteur_index_uris = (
        a['href'] for a in chain.from_iterable(
            ul('a', href=True) for ul in index_soup('ul', 'typepersonne')
        )
    )
    auteur_uris = (
        a['href'] for a in chain.from_iterable(
            get_soup(uri)('a', 'auteur', href=True) for uri in auteur_index_uris
        ) if a.has_key('href')
    )
    numero_uris = (
        a['href'] for a in chain.from_iterable(
            ul('a', href=True) for ul in index_soup('ul', 'issues')
        ) if a.has_key('href')
    )
    article_uris = set(chain(
        numero_uris,
        (a['href'] for a in chain.from_iterable(
            dl('a', href=True) for dl in chain.from_iterable(
                get_soup(uri)('dl', 'listArticles') for uri in auteur_uris
            )
        ) if a.has_key('href')),
        (a['href'] for a in chain.from_iterable(
            ul('a', href=True) for ul in chain.from_iterable(
                get_soup(uri)('ul', 'summary') for uri in numero_uris
            )
        ) if a.has_key('href'))
    ))
    nodes = [get_node(uri) for uri in article_uris]
    return nodes
