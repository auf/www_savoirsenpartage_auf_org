# -*- encoding: utf-8 -*-
import urllib, httplib, time, simplejson, pprint, math, re
from django.conf import settings
from auf_savoirs_en_partage_backend.sep.io import SEP
from auf_savoirs_en_partage_backend.sep.utils import smart_str
from savoirs import configuration


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
    content = regexp.sub (r'<b>\1</b>', content)
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
    patt = "([\W]{1})(" + patt + ")([\W]{1})"
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
        uri = r.get ("source", "")
        if len (uri) == 0:
            uri = r.get ("uri")

        title = regexp.sub (r'<b>\1</b>', r.get ("title", ""))

        content = sep_build_content (regexp, r.get ("description", ""))

        contributeurs = r.get('contributor')
        if contributeurs is not None:
            contributeurs = "; ".join (contributeurs)

        subject = r.get ('subject')
        if subject is not None:
            subject = ", ".join (subject)

        data['results'].append ({'uri': uri, 
                'id': r.get("uri"), \
                'title': hl(regexp, title), 
                'content': hl(regexp, content), \
                'creator': '; '.join([hl(regexp, x) for x in r.get('creator')]),
                'contributors': hl(regexp, contributeurs),
                'subject': hl(regexp, subject),
                'modified': r.get('modified'),
                'isbn': r.get('isbn'),
                })


def cherche (page, q, engin=None):
    rc = {'results': [], 'last_page': 0, 'more_link': ''}

    if engin is None:
        engin = configuration['engin_recherche']

    if engin == 'google':
        google_search (page, q, rc)

    elif engin == 'sep':
        sep_search (page, {'q': q.encode ('utf-8')}, rc)

    elif engin == 'avancee':
        sep_search (page, q, rc)
    
    return rc
