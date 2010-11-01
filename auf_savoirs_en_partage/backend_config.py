# -*- encoding: utf-8 -*-

### Configuration de SEP

# Sources de données
RESOURCES = {

    #OAI
    
    u'aide-en-ligne': {
        'type': 'oai',
        'acces': 'generic',
        'url': 'http://eprints.aidenligne-francais-universite.auf.org/',
    },
    u'Centredoc-Org': {
        'type': 'oai',
        'acces': 'generic',
        'url': 'http://doc.refer.org/',
    },
    u'Bibliothèque Numérique de Ouagadougou': {
        'type': 'oai',
        'acces': 'generic',
        'url': 'http://greenstone.bf.refer.org/'
    },
    u'Centredoc-Fr': {
        'type': 'oai',
        'acces': 'generic',
        'url': 'http://auf.centredoc.fr/ws/PMBOAI_1/'
    },
    u'CRITAOI': {
        'type': 'oai',
        'acces': 'generic',
        'url': 'http://biblio.critaoi.auf.org/'
    },
    u'Archives ouvertes du Moyen-Orient': {
        'type': 'oai',
        'acces': 'generic',
        'url': 'http://hal-confremo.archives-ouvertes.fr/'
    },
    u'CECA': {
        'type': 'oai',
        'acces': 'generic',
        'url': 'http://ceca.auf.org/',
    },

    #LODEL
    u'Revue-signes': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.revue-signes.info/',
    },
    u'ERGI': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.revue-genie-industriel.info/',
    },
    u'e-Santé': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.revue-esante.info/',
    },
    u'Radisma': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.radisma.info/',
    },
    u'RMNSci.net': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.rmnsci.net/',
    },
    u'Urbamag': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.urbamag.net/',
    },
    u'Afrique Science': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.afriquescience.info/',
    },
    u'e-Ti': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.revue-eti.net/',
    },
    u'Taloha': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.taloha.info/',
    },
    u'TDR': {
        'type': 'lodel',
        'acces': 'html',
        'url': 'http://www.revue-tice.info/',
    },
    #'Exchorésis': {
    #    'type': 'lodel',
    #    'acces': 'html',
    #    'url': 'http://exchoresis.refer.ga/',
    #},

    # SPIP
    #'Annales des sciences agronomiques du Bénin': {
    #    'type': 'lodel', 
    #    'acces': 'html',
    #    'url': 'http://www.annales-fsa.bj.refer.org/',
    #},

    # SPIP
    #'Bulletin des OSCB': {
    #    'type': 'lodel',
    #    'acces': 'html',
    #    'url': 'http://www.osc.bj.refer.org/',
    #},
}