# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.forms.formsets import formset_factory
from .forms import TruckForm, BaseMenuFormSet, MenuForm

import logging
import utils

# set up logging
logging.basicConfig(filename='/home/ec2-user/website.log',level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

def index(request):
    context = {}
    return render(request, 'wheelappeal/index.html', context)

def api(request):
    return HttpResponse('This is our API. It is currently under construction.')

# def submit(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         form = TruckForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             print form
#             return HttpResponseRedirect('/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = TruckForm()
#
#     return render(request, 'wheelappeal/submit.html', {'form': form})

def submit(request):
    """
    Allows a user to update their own profile.
    """
    # Create the formset, specifying the form and formset we want to use.
    MenuFormSet = formset_factory(MenuForm, formset=BaseMenuFormSet)

    if request.method == 'POST':
        truck_form = TruckForm(request.POST)
        menu_formset = MenuFormSet(request.POST)

        if truck_form.is_valid() and menu_formset.is_valid():
            logging.debug("Menu and truck forms are valid")
            truck_name = truck_form.cleaned_data.get('truck_name')
            cuisine = truck_form.cleaned_data.get('cuisine')
            logging.debug("Submit request: %s, %s" % (truck_name, cuisine))
            menu_items = []

            for menu_form in menu_formset:
                item_name = menu_form.cleaned_data.get('item_name')
                item_price = menu_form.cleaned_data.get('item_price')

                if item_name and item_price:
                    menu_items.append({'name':item_name, 'price':item_price})
                else:
                    logging.debug("Missing menu fields for %s: %s, %s," % (truck_name, item_name, item_price))
                    return HttpResponse("It looks like you missed a field in the menu!")
            # try:
            #     with transaction.atomic():
            #         #Replace the old with the new
            #         UserLink.objects.filter(user=user).delete()
            #         UserLink.objects.bulk_create(new_links)
            #
            #         # And notify our users that it worked
            #         messages.success(request, 'You have submitted your information.')

            # except IntegrityError: #If the transaction failed
            #     messages.error(request, 'There was an error saving your profile.')
            #     return redirect(reverse('profile-settings'))
            truck_data = {'truck_name':truck_name, 'cuisine':cuisine, 'menu': menu_items}
            response = utils.post_truck_data(truck_data)
            if response:
                return HttpResponse('Successful Post')
            else:
                logging.debug("Error in truck submission: %s" % (response))
                return HttpResponse("ERROR!! " + response.text)
    else:
        truck_form = TruckForm()
        menu_formset = MenuFormSet()

    context = {
        'truck_form': truck_form,
        'menu_formset': menu_formset,
    }
    
    return render(request, 'wheelappeal/submit.html', context)
