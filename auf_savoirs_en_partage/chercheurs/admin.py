# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin

from models import *

admin.site.register(Chercheur)
admin.site.register(Publication)
admin.site.register(Groupe)

