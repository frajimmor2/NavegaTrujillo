from django import forms


class ShipForm(forms.Form):
    available = forms.BooleanField(required = False)
    rent_per_day = forms.FloatField(required = True)
    capacity = forms.IntegerField(required = True)
    needs_license = forms.BooleanField(required = False)
    description = forms.CharField(required = True)

class ReservationForm(forms.Form):
    captain = forms.BooleanField(required = False)
