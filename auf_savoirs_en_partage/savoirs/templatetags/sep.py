# -*- encoding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils.encoding import smart_str
from datamaster_modeles.models import Region
from savoirs.models import Discipline

def sep_menu(discipline_active, region_active):
    regions = Region.objects.filter(actif=True).order_by('nom')
    disciplines = Discipline.objects.all()
    return dict(disciplines=disciplines, regions=regions,
                discipline_active=discipline_active, region_active=region_active)

register = template.Library()
register.inclusion_tag('menu.html')(sep_menu)

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
        if kwargs.get('discipline') == 'all':
            del kwargs['discipline']
        else:
            context_discipline = context.get('discipline_active')
            if context_discipline:
                kwargs.setdefault('discipline', context_discipline)
        if kwargs.get('region') == 'all':
            del kwargs['region']
        else:
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

def sep_url(parser, token):
    """
    Le tag ``url`` de Django, modifié pour SEP.

    Lorsque ce tag est utilisé, la discipline et la région actives sont
    automatiquement réinjectées dans les URL construites.

    On peut annuler cette réinjection en spécifiant l'argument
    ``region='all'`` ou ``discipline='all'``.
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
sep_url = register.tag(sep_url)
