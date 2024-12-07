from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from business.models import Ship, Port

class ShipForm(forms.ModelForm):
    ''' Formulario de cambio de datos de barcos '''

    class Meta:
        model = Ship
        fields = ['available', 'rent_per_day', 'capacity', 'need_license', 'description']


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
    captain = forms.BooleanField(required = False,widget=forms.HiddenInput())
    captain.disabled = True

class ReservationDataHiddenForm(forms.Form):
    captain = forms.BooleanField(required = False,widget=forms.HiddenInput())
    captain.disabled = True


class shopping_basket_form(forms.Form):
    captain = forms.BooleanField()

class dates_form(forms.Form):
    rent_start_day = forms.DateField(label="Fecha de inicio de la reserva", widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}), required= False)
    rent_end_day = forms.DateField(label="Fecha de fin de la reserva", widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}), required=False)
    name_form = forms.CharField(label="Nombre del barco", widget=forms.TextInput, required=False)


    def clean(self):
        cleaned_data = super().clean()
        rent_start_day = cleaned_data.get('rent_start_day')
        rent_end_day = cleaned_data.get('rent_end_day')

        # Si una fecha está presente, la otra también debe estarlo
        if rent_start_day and not rent_end_day:
            raise ValidationError("Debe especificar una fecha de fin si proporciona una fecha de inicio.")
        if rent_end_day and not rent_start_day:
            raise ValidationError("Debe especificar una fecha de inicio si proporciona una fecha de fin.")

        # Verificar que la fecha de fin sea igual o posterior a la de inicio
        if rent_start_day and rent_end_day:
            if rent_end_day < rent_start_day:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")

        return cleaned_data
