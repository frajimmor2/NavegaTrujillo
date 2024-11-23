from django import forms


class ShipForm(forms.Form):
    ''' Formulario de cambio de datos de barcos '''

    available = forms.BooleanField(required = False)
    rent_per_day = forms.FloatField(required = True)
    capacity = forms.IntegerField(required = True)
    needs_license = forms.BooleanField(required = False)
    description = forms.CharField(required = True)


class ReservationForm(forms.Form):
    ''' Formulario de reserva (capitán o no) '''

    captain = forms.BooleanField(required = False)


class ReservationFormNotLogged(forms.Form):
    ''' Formulario de reserva obligado '''

    captain = forms.BooleanField(required = True)
    captain.initial = True
    captain.disabled = True

class ReservationDataForm(forms.Form):
    ''' Formulario de toma de datos (usuario no autentificado) '''

    Email = forms.EmailField(required = True)
    name = forms.CharField(required = True)
    surname = forms.CharField(required = True)
