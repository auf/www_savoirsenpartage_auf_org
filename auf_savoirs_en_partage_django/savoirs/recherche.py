# -*- encoding: utf-8 -*-
import urllib, httplib, time, simplejson, pprint, math, re
from auf_savoirs_en_partage_backend.sep.io import SEP
from savoirs import configuration

def google_search (page, q, data):
    params = {'q': q,
              'rsz': 'large',
              'v': '1.0',
              'start': page * configuration['resultats_par_page'],
              #'cref': "http://savoirsenpartage.auf.org/recherche.xml?%s" % int(time.time())
              }
    url = "/ajax/services/search/web?" + \
            urllib.urlencode (params)
    handle = httplib.HTTPConnection ('ajax.googleapis.com')
    handle.request ("GET", url)
    r = handle.getresponse ()
    response = simplejson.loads(r.read ())
    print pprint.pformat (params)
    print pprint.pformat (response)
    handle.close ()

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
    if len (description) > maxlen:
        loc = regexp.search (description)
        f = loc.start () - (maxlen / 2)
        t = 0
        if f < 0:
            t = -f
            f = 0
        t += loc.start () + (maxlen / 2)
        if f > 0:
            while description[f] != '.' and f > 0:
                f -= 1
            if f > 0:
                f += 1
        if t < len (description):
            while description[t] != '.' and t < len (description):
                t += 1
            t += 1
        content = description[f:t]
        if f > 0:
            content = "(...) " + content
        if t < (len (description) - 1):
            content = content + " (...)"
    content = regexp.sub (r'<b>\1</b>', content)
    return content


def sep_search (page, q, data):
    f = page * configuration['resultats_par_page']
    t = f + 8
    s = SEP ()
    matches = s.search ({'description': q.encode ('utf-8')})
    data['last_page'] = math.ceil (float(len (matches)) / \
            float(configuration['resultats_par_page'])) - 1
    set = s.get (matches[f:t])
    regexp = re.compile (r'(%s)' % q, re.IGNORECASE)
    for r in set:
        uri = r.get ("source", "")
        if len (uri) == 0:
            uri = r.get ("uri")
        title = r.get ("title", "")
        tmp = r.get ("description", "")
        content = sep_build_content (regexp, tmp)

        data['results'].append ({'uri': uri, 'title': title, 'content': content})

    #data['results'] = s.get (matches[f:t])

def cherche (engin, page, q):
    rc = {'results': [], 'last_page': 0, 'more_link': ''}
    lastp = 0

    if engin == 'google':
        google_search (page, q, rc)

    elif engin == 'sep':
        sep_search (page, q, rc)
    
    return rc
