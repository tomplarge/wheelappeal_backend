# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .forms import TruckForm

def index(request):
    context = {}
    return render(request, 'wheelappeal/index.html', context)

def api(request):
    return HttpResponse('This is our API. It is currently under construction.')

def submit(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # get the menu items that were added
        menu = get_menu(request)
        # create a form instance and populate it with data from the request:
        form = TruckForm(request.POST, menu=menu)
        # check whether it's valid:
        if form.is_valid():
            for unknown in form.:
                save_answer(request, question, answer)
            print "Form is good!"
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TruckForm()

    return render(request, 'wheelappeal/submit.html', {'form': form})

def get_menu(request):
    return
