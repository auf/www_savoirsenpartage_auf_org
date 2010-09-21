# -*- encoding: utf-8 -*-
import datetime, simplejson, copy, vobject

from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


from lib.recherche import cherche, google_search
from lib import sep
from lib.calendrier import evenements, evenement_info, evenement_publie, combine
from savoirs.globals import configuration
import backend_config
from forms import *
from models import *
from chercheurs.models import Chercheur
from sitotheque.models import Site


def index (request):
    delta = datetime.timedelta (days = 90)
    oldest = datetime.date.today () - delta
    articles = Actualite.objects.filter (visible = '1', date__gt = oldest)
    articles = articles[0:configuration['accueil_actualite']]
    try:
        events = evenements()[0:configuration['accueil_evenement']]
    except:
        events = []
    chercheurs = Chercheur.objects.all().order_by('?')[:configuration['accueil_chercheur']]
    sites = Site.objects.all().order_by('?')[:configuration['accueil_sites']]
    return render_to_response ("savoirs/index.html", \
            Context ({"articles": articles,
                      "events": events,
                      "caldav_url": configuration['calendrier_publique'],
                      "chercheurs":chercheurs,
                      "sites":sites,
                      }), \
            context_instance = RequestContext(request))

def recherche (request):
    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 0))

    r = cherche (page, q)

    return render_to_response ("savoirs/recherche.html", \
            Context ({'q': q,
                      'page': page,
                      'data': r}), \
            context_instance = RequestContext(request))

def avancee (request):
    type = request.GET.get("type", "")
    page = int(request.GET.get("page", 0))

    r = {'results': [], 'last_page': 0, 'more_link': ''}

    q = request.GET.get("google-q", "")
    f = RechercheAvancee ()

    if type == 'google':
        r = cherche (page, q, type)
        q = {'q': q}
    elif type == 'avancee':
        f = RechercheAvancee (request.GET)
        if f.is_valid():
            q = {}
            for k in ['creator', 'title', 'description', 'subject']:
                tmp = f.cleaned_data[k].strip()
                if len (tmp) > 0:
                    q[k] = tmp
            q['operator'] = '|'
            if f.cleaned_data['operator'] == 'and':
                q['operator'] = "&"

            r = cherche (page, q, type)

    return render_to_response ("savoirs/avancee.html", \
            Context ({'type': type,
                      'page': page,
                      'data': r,
                      'form': f,
                      'q': q}), 
            context_instance = RequestContext(request))

def conseils (request):
    return render_to_response ("savoirs/conseils.html", \
            Context (), \
            context_instance = RequestContext(request))

def a_propos (request):
    return render_to_response ("savoirs/a-propos.html", \
            Context ({'count': len(backend_config.RESOURCES)}), \
            context_instance = RequestContext(request))

def informations (request):
    s = sep.SEP()
    resources = copy.deepcopy (backend_config.RESOURCES)
    for k in backend_config.RESOURCES.keys ():
        try:
            resources[k]['logs'] = { 'date': t[k][0], 'count': t[k][1] }
        except: pass

    logs = HarvestLog.objects.filter(context = 'moisson').order_by('date')
    for l in logs:
        resources[l.name]['logs'] = {'date' : l.date, 'count': l.processed}

    return render_to_response ("savoirs/informations.html", \
            Context ({'r': resources}), \
            context_instance = RequestContext(request))

def nous_contacter (request):
    return render_to_response ("savoirs/contact.html", \
            Context (), \
            context_instance = RequestContext(request))


def evenement(request, id):
    event = evenement_info(id)
    return render_to_response ("savoirs/evenement.html", \
            Context ({'event': event.instance.vevent}), \
            context_instance = RequestContext(request))

def evenement_ajout(request):
    template = "savoirs/evenement_ajout.html"
    if request.method == "POST":
        form = EvenementForm(request.POST)
        if form.is_valid():
            form.save()
            template = "savoirs/evenement_confirmation.html"
    else:
        form = EvenementForm()
    return render_to_response (template, \
                               Context ({'form': form}), \
                               context_instance = RequestContext(request))

@login_required
def evenement_moderation(request):
    events = Evenement.objects.filter(approuve = False)
    return render_to_response ("savoirs/evenement_moderation.html", \
                               Context ({'events': events}), \
                               context_instance = RequestContext(request))

@login_required
def evenement_accepter(request, pk):
    e = Evenement.objects.get(pk = pk)

    cal = vobject.iCalendar()
    cal.add('vevent')
    cal.vevent.add('summary').value = e.titre
    
    kw = e.mots_cles.split(",")
    try:
        kw.append(e.discipline.nom)
        kw.append(e.discipline_secondaire.nom)
        kw.append(e.type)
    except: pass

    kw = [x.strip() for x in kw if len(x.strip()) > 0]
    for k in kw:
        cal.vevent.add('x-auf-keywords').value = k

    if len(kw) > 0:
        if len(e.description) > 0:
            e.description += "\n"
        e.description += u"Mots-cles: " + ", ".join(kw)

    cal.vevent.add('dtstart').value = combine(e.debut, e.fuseau)
    cal.vevent.add('dtend').value = combine(e.fin, e.fuseau)
    cal.vevent.add('created').value = combine(datetime.datetime.now(), "UTC")
    cal.vevent.add('dtstamp').value = combine(datetime.datetime.now(), "UTC")
    if len(e.description) > 0:
        cal.vevent.add('description').value = e.description
    if len(e.contact) > 0:
        cal.vevent.add('contact').value = e.contact
    if len(e.url) > 0:
        cal.vevent.add('url').value = e.url
    if len(e.lieu) > 0:
        cal.vevent.add('location').value = e.lieu

    evenement_publie(cal)

    e.actif = False
    e.save()

    return HttpResponseRedirect(reverse('savoirs.views.evenement_moderation'))

@login_required
def evenement_refuser(request, pk):
    evenement = Evenement.objects.get(pk = pk)
    evenement.actif = False
    evenement.save()
    return HttpResponseRedirect(reverse('savoirs.views.evenement_moderation'))


@login_required
def json_get (request):
    uri = request.GET.get ("uri")
    if uri:
        s = sep.SEP ()
        res = s.search ({'uri': uri.encode("utf-8")})
        r = s.get (res)
    
        return HttpResponse(simplejson.dumps(r[0]),
            mimetype='application/json')

@login_required
def json_set (request):
    data = request.POST.get("data")
    if data:
        r = simplejson.loads(data)
        s = sep.SEP ()
        s.add (r)
    return HttpResponse(simplejson.dumps("OK"),
            mimetype='application/json')
