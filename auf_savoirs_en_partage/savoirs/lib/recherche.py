# -*- encoding: utf-8 -*-
import urllib, httplib, time, simplejson, pprint, math, re
from django.core.urlresolvers import reverse
from django.conf import settings
from auf_savoirs_en_partage.backend_config import RESOURCES
from sep import SEP
from utils import smart_str
from savoirs.globals import configuration

def google_search (page, q, data):
    params = {'q': q,
              'rsz': 'large',
              'v': '1.0',
              'start': page * configuration['resultats_par_page'],
              }

    params['cref'] = configuration['google_xml'] % time.time()
    url = "/ajax/services/search/web?" + urllib.urlencode (params)

    handle = httplib.HTTPConnection ('ajax.googleapis.com')
    handle.request ("GET", url)
    r = handle.getresponse ()
    response = simplejson.loads(r.read ())
    #print pprint.pformat (params)
    #print pprint.pformat (response)
    handle.close ()

    if len (response['responseData']['results']) > 0:
        for i in response['responseData']['cursor']['pages']:
            p = int (i['label']) - 1
            if p > data['last_page']:
                data['last_page'] = p

        for r in response['responseData']['results']:
            data['results'].append( {'uri': r['url'],
                        'content': r['content'],
                        'title': r['title']} )

        data['more_link'] = response['responseData']['cursor']['moreResultsUrl']


def sep_build_content (regexp, description):
    maxlen = 200
    content = description
    if len (description) > maxlen:
        start = 0
        loc = regexp.search (description)
        if loc:
            start = loc.start ()

        f = start - (maxlen / 2)
        t = 0
        if f < 0:
            t = -f
            f = 0
        t += start + (maxlen / 2)
        if f > 0:
            while description[f] != '.' and f > 0:
                f -= 1
            if f > 0:
                f += 1
        if t < len (description):
            while t < len (description) and description[t] != '.':
                t += 1
            t += 1
        content = description[f:t]
        if f > 0:
            content = "(...) " + content
        if t < (len (description) - 1):
            content = content + " (...)"
    content = regexp.sub (r'\1<b>\2</b>\3', content)
    return content


def make_regexp (q):
    words = []
    w = re.compile (r'\W+', re.U)
    for k in q.keys ():
        if k != 'operator':
            words.extend(w.split (smart_str(q[k]).decode("utf-8")))
    words = filter (lambda x: len(x)>2, words)
    words.sort (lambda x,y: len(y)-len(x))

    patt = "|".join (words)
    patt = "([\W|-]{1})(" + patt + ")([\W|-]{1})"
    return re.compile (patt, re.I|re.U)

def hl (r, string):
    if string is not None:
        return r.sub (r'\1<b>\2</b>\3', string)
    return None


def sep_search (page, q, data):
    f = page * configuration['resultats_par_page']
    t = f + 8
    s = SEP ()

    matches = s.search (q)
    data['last_page'] = math.ceil (float(len (matches)) / \
            float(configuration['resultats_par_page'])) - 1
    set = s.get (matches[f:t])
    regexp = make_regexp (q)

    for r in set:
        uri = r.get ("uri", "")
        if len (uri) == 0:
            uri = r.get ("source")
        
        serveur = RESOURCES[r.get('server')]['url']

        # Récupère la source si ce n'est pas une URL
        source = r.get("source", None)
        if source is not None and source.startswith('http'):
            source = None

        title = r.get ("title", "")
        content = sep_build_content (regexp, r.get ("description", ""))

        contributeurs = r.get('contributor')
        if contributeurs is not None:
            contributeurs = "; ".join (contributeurs)

        subject = r.get ('subject')
        if subject is not None:
            subject = ", ".join (subject)

        data['results'].append ({
                'uri': uri,
                'getServeurURL': serveur,
                'source' : source,
                'id': r.get("id"), \
                'title': hl(regexp, title), 
                'content': content, \
                'creator': '; '.join([hl(regexp, x) for x in r.get('creator', [])]),
                'contributors': hl(regexp, contributeurs),
                'subject': hl(regexp, subject),
                'modified': r.get('modified'),
                'isbn': r.get('isbn'),
                'admin_url': reverse('admin:savoirs_record_change', args=[r.get('id')])
                })


def cherche (page, q, engin=None):
    rc = {'results': [], 'last_page': 0, 'more_link': ''}

    if engin is None:
        engin = configuration['engin_recherche']

    if engin == 'google':
        google_search (page, q, rc)

    elif engin == 'sep':
        sep_search (page, {'q': q}, rc)

    elif engin == 'avancee':
        sep_search (page, q, rc)
    
    return rc

def build_search_regexp(query):
    """Construit une expression régulière qui peut servir à chercher les
       mots-clés donnés dans 'query'."""
    words = query.split()
    if not words:
        return None
    parts = []
    for word in words:
        part = re.escape(word.lower())
        # Les expressions régulières ne connaissent pas la version
        # en majuscules des caractères accentués.  :(
        part = part.replace(u'à', u'[àÀ]')
        part = part.replace(u'â', u'[âÂ]')
        part = part.replace(u'é', u'[éÉ]')
        part = part.replace(u'ê', u'[êÊ]')
        part = part.replace(u'î', u'[îÎ]')
        part = part.replace(u'ç', u'[çÇ]')

        # Faire ceci après avoir traité les caractères accentués...
        part = part.replace('a', u'[aàâÀÂ]')
        part = part.replace('e', u'[eéèëêÉÊ]')
        part = part.replace('i', u'[iïîÎ]')
        part = part.replace('o', u'[oô]')
        part = part.replace('u', u'[uûüù]')
        part = part.replace('c', u'[cç]')

        parts.append(part)
    return re.compile('|'.join(parts), re.I) 
