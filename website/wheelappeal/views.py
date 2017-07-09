# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    # template = loader.get_template('static/index.html')
    context = {}
    return render(request, 'wheelappeal/index.html',context)

def api(request):
    return HttpResponse('This is our API. It is currently under construction.')
