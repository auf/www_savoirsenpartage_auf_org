#!/usr/bin/env python
# -*- encoding: utf-8 -*-

configuration = {
    'max_actualite': 100,
    'accueil_actualite': 5,
    'accueil_chercheur': 6,
    'nombre_par_page_actualite': 10,
    'resultats_par_page': 8, # pas changeable a cause de google
    'accueil_evenement': 10,
    'engin_recherche': 'sep',
    'google_xml': "http://www.savoirsenpartage.auf.org/recherche.xml?%s",
    'calendrier_publique': 'http://cal.ro.auf.org/caldav.php/davin/test/',
}

#####
# Meta fields
TITLE           = 'title'
ALT_TITLE       = 'alt_title'
CREATOR         = 'creator'
CONTRIBUTOR     = 'contributor'
DESCRIPTION     = 'description'
ABSTRACT        = 'abstract'
SUBJECT         = 'subject'
PUBLISHER       = 'publisher'
DATE_CREATION   = 'creation'
DATE_ISSUED     = 'issued'
DATE_MODIFIED   = 'modified'
TYPE            = 'type'
FORMAT          = 'format'
IDENTIFIER      = 'identifier'
ISBN            = 'isbn'
URI             = 'uri'
SOURCE          = 'source'
LANGUAGE        = 'language'
ORIG_LANG       = 'orig_lang'


META = {TITLE: {'type': 'text', 'text_search': True},
        ALT_TITLE: {'type': 'text', 'text_search': True},
        CREATOR: {'type': 'array', 'text_search': True},
        CONTRIBUTOR: {'type': 'array', 'text_search': True},
        DESCRIPTION: {'type': 'text', 'text_search': True},
        ABSTRACT: {'type': 'text', 'text_search': True},
        SUBJECT: {'type': 'array', 'text_search': True},
        PUBLISHER: {'type': 'array'},
        DATE_CREATION: {'type': 'date'},
        DATE_ISSUED: {'type': 'date'},
        DATE_MODIFIED: {'type': 'date'},
        TYPE: {'type': 'array'},
        FORMAT: {'type': 'array'},
        IDENTIFIER: {'type': 'text'},
        ISBN: {'type': 'text'},
        URI: {'type': 'text', 'unique': True},
        SOURCE: {'type': 'text'},
        LANGUAGE: {'type': 'array'},
        ORIG_LANG: {'type': 'array'}
        }
