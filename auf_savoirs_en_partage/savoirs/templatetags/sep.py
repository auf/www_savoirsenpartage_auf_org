# -*- encoding: utf-8 -*-

import re
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from auf.django.references.models import Region
from savoirs.models import Discipline

register = template.Library()

@register.inclusion_tag('menu.html', takes_context=True)
def sep_menu(context, discipline_active, region_active):
    regions = Region.objects.filter(actif=True).order_by('nom')
    disciplines = Discipline.objects.all()
    return dict(disciplines=disciplines, regions=regions,
                discipline_active=discipline_active, region_active=region_active,
                request=context['request'])

@register.inclusion_tag('menu_brique.html', takes_context=True)
def sep_menu_brique(context, discipline_active, region_active):
    regions = Region.objects.filter(actif=True).order_by('nom')
    disciplines = Discipline.objects.all()
    return dict(disciplines=disciplines, regions=regions,
                discipline_active=discipline_active, region_active=region_active,
                request=context['request'])

@register.inclusion_tag('sort_link.html', takes_context=True)
def sort_link(context, field, label):
    request = context['request']
    params = request.GET.copy()
    current_sort = params.get('tri')
    if current_sort == field:
        sort = field + '_desc'
        indicator = u' (croissant)'
    else:
        sort = field
        if current_sort == field + '_desc':
            indicator = u' (décroissant)'
        else:
            indicator = ''

    params['tri'] = sort
    url = request.path + '?' + params.urlencode()
    return dict(label=label, url=url, indicator=indicator)

class URLNode(template.Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        # C'est ici que nous injectons la discipline et la région courante
        # dans les arguments.
        context_discipline = context.get('discipline_active')
        if context_discipline:
            kwargs.setdefault('discipline', context_discipline)
        context_region = context.get('region_active')
        if context_region:
            kwargs.setdefault('region', context_region)

        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = reverse(self.view_name, args=args, kwargs=kwargs, current_app=context.current_app)
        except NoReverseMatch, e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse(project_name + '.' + self.view_name,
                              args=args, kwargs=kwargs, current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

@register.tag
def sep_url(parser, token):
    """
    Le tag ``url`` de Django, modifié pour SEP.

    Lorsque ce tag est utilisé, la discipline et la région actives sont
    automatiquement réinjectées dans les URL construites.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    asvar = None

    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))
    return URLNode(viewname, args, kwargs, asvar)

DISCIPLINE_REGION_RE = re.compile(r'(/discipline/\d+)?(/region/\d+)?')

@register.filter
@stringfilter
def change_region(path, region):
    """Modifie la région dans le chemin donné."""
    match = DISCIPLINE_REGION_RE.match(path)
    discipline_bit = match.group(1) or ''
    region_bit = '/region/%d' % region if region != 'all' else ''
    rest = path[match.end():]
    if not rest.startswith('/recherche/'):
        rest = '/'
    return discipline_bit + region_bit + rest

@register.filter
@stringfilter
def change_discipline(path, discipline):
    """Modifie la discipline dans le chemin donné."""
    match = DISCIPLINE_REGION_RE.match(path)
    discipline_bit = '/discipline/%d' % discipline if discipline != 'all' else ''
    region_bit = match.group(2) or ''
    rest = path[match.end():]
    if not rest.startswith('/recherche/'):
        rest = '/'
    return discipline_bit + region_bit + rest


@register.filter
def apply(value, func):
    """Applique une fonction arbitraire à la valeur filtrée."""
    return func(value)

@register.filter
def getitem(container, key):
    """Applique ``container[key]`` sur la valeur filtrée."""
    return container.get(key, '')


# Snippet: http://djangosnippets.org/snippets/2237/
@register.tag
def query_string(parser, token):
    """
    Allows you too manipulate the query string of a page by adding and removing keywords.
    If a given value is a context variable it will resolve it.
    Based on similiar snippet by user "dnordberg".

    requires you to add:

    TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    )

    to your django settings.

    Usage:
    http://www.url.com/{% query_string "param_to_add=value, param_to_add=value" "param_to_remove, params_to_remove" %}

    Example:
    http://www.url.com/{% query_string "" "filter" %}filter={{new_filter}}
    http://www.url.com/{% query_string "page=page_obj.number" "sort" %}

    """
    try:
        tag_name, add_string,remove_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    if not (add_string[0] == add_string[-1] and add_string[0] in ('"', "'")) or not (remove_string[0] == remove_string[-1] and remove_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

    add = string_to_dict(add_string[1:-1])
    remove = string_to_list(remove_string[1:-1])

    return QueryStringNode(add,remove)

class QueryStringNode(template.Node):
    def __init__(self, add,remove):
        self.add = add
        self.remove = remove

    def render(self, context):
        p = {}
        for k, v in context["request"].GET.items():
            p[k]=v
        return get_query_string(p,self.add,self.remove,context)

def get_query_string(p, new_params, remove, context):
    """
    Add and remove query parameters. From `django.contrib.admin`.
    """
    for r in remove:
        for k in p.keys():
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if k in p and v is None:
            del p[k]
        elif v is not None:
            p[k] = v

    for k, v in p.items():
        try:
            p[k] = template.Variable(v).resolve(context)
        except:
            p[k]=v

    return mark_safe('?' + '&amp;'.join([u'%s=%s' % (k, v) for k, v in p.items()]).replace(' ', '%20'))

# Taken from lib/utils.py
def string_to_dict(string):
    kwargs = {}

    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '': continue
            kw, val = arg.split('=', 1)
            kwargs[kw] = val
    return kwargs

def string_to_list(string):
    args = []
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '': continue
            args.append(arg)
    return args
