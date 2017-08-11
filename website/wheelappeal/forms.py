from django import forms

class TruckForm(forms.Form):
    truck_name = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Truck Name'}))
    cuisine = forms.CharField(max_length=100,  required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Cuisine'}))

    def __init__(self, *args, **kwargs):
        menu_items = kwargs.pop('menu')
        super(TruckForm, self).__init__(*args, **kwargs)

        for unknown in enumerate(extra):
            print unknown
            #self.fields['custom_%s' % i] = forms.CharField(required=True)

    def menu_items(self):
            for name, value in self.cleaned_data.items():
                if name.startswith('custom_'):
                    yield (self.fields[name].label, value)
