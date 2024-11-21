from django import forms


class ShipForm(forms.Form):
    ''' Formulario de cambio de datos de barcos '''

    available = forms.BooleanField(required = False)
    rent_per_day = forms.FloatField(required = True)
    capacity = forms.IntegerField(required = True)
    needs_license = forms.BooleanField(required = False)
    description = forms.CharField(required = True)

class ReservationForm(forms.Form):
    ''' Formulario para reserva rápida, solo interesa si tiene capitán o no 
        (falta forzar en caso de que se necesite licencia y o no se tenga o no se esté logueado)'''

    captain = forms.BooleanField(required = False)
