from django import forms


class ShipForm(forms.Form):
    available = forms.BooleanField(required = True)
    rent_per_day = forms.FloatField(required = True)
    capacity = forms.IntegerField(required = True)
    needs_license = forms.BooleanField(required = True)
    description = forms.CharField(required = True)

class shopping_basket_form(forms.Form):
    captain = forms.BooleanField()