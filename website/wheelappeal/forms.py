from django import forms
from django.forms.formsets import BaseFormSet

class TruckForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TruckForm, self).__init__(*args, **kwargs)
        self.fields['truck_name'] = forms.CharField(max_length=100, required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Truck Name'}))
        self.fields['cuisine'] = cuisine = forms.CharField(max_length=100, required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Cuisine'}))

class MenuForm(forms.Form):
    item_name = forms.CharField(max_length = 50, required=True,
        widget=forms.TextInput(attrs = {'placeholder': 'Item','class':'item-name'}))
    item_price = forms.FloatField(required=True,
        widget=forms.TextInput(attrs = {'placeholder': 'Price','class':'item-price'}))

class BaseMenuFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        items = []
        prices = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['item_name']
                price = form.cleaned_data['item_price']
                # Check that no menu items have the same name
                if name and price:
                    prices.append(price)
                    if name in items:
                        duplicates = True
                    items.append(name)

                if duplicates:
                    # will spaces have an effect here?
                    raise forms.ValidationError(
                        'Menu items must have unique names',
                        code='duplicate_items'
                    )

                # Check that all menu items have both name and price
                if name and not price:
                    raise forms.ValidationError(
                        'All menu items must have a name and a price.',
                        code='missing_price'
                    )
                elif price and not name:
                    raise forms.ValidationError(
                        'All menu items must have a name and a price.',
                        code='missing_name'
                    )
