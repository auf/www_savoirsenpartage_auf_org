# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

def page_404(request):
    return render_to_response("404.html", context_instance = RequestContext(request))

def page_500(request):
    return render_to_response("500.html", context_instance = RequestContext(request))
