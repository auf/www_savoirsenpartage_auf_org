# -*- encoding: utf-8 -*-
from savoirs.globals import *

# From django
def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    elif not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def safe_append (dict, key, value):
    """Ajoute la valeur `value` à la liste contenue dans `dict[key]`. 
    Créée la liste au besoin.
    """
    try:
        list = dict[key]
    except:
        dict[key] = []
    dict[key].append (value)

def meta_set (meta, field, value):
    """Ajoute la valeur `value` à la structure de métadonnées `meta`, en 
    fonction de son type.
    """
    f = META.get (field, None)
    if f is not None:
        if f['type'] == 'text':
            meta[field] = smart_str(value)
        elif f['type'] == 'array':
            safe_append (meta, field, value)


def print_structure(element, tab=""):
    """Méthode de debug, permet d'afficher l'arborescence d'un XMLTree (lxml)
    """
    if element.text:
        element.text = element.text.strip ()
    if element.tail:
        element.tail = element.tail.strip ()
    line = u"%s<%s>: %s, %s, %s" % (tab, element.tag, element.text, 
        element.tail, element.attrib)
    print line.encode ("utf-8")
    for x in element.getchildren():
        print_structure(x, tab+" ")

def find_text (node, tag):
    """Trouve la valeur du texte contenue dans le premier descendant de `node` 
    ayant comme tag `tag`.
    """
    rc = ""
    n = node.find (".//%s" % tag)
    if n is not None:
        rc = n.text
    return rc
