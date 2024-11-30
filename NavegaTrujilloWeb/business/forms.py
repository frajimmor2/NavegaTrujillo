from django import forms
from django.utils import timezone
import datetime
class ReservationTimeForm(forms.Form):
    ''' Formulario de plazo de reserva: fecha inicio y fecha fin '''
    start_date = forms.DateField(required=True,widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(required=True,widget=forms.DateInput(attrs={'type':'date'}))
    captain = forms.BooleanField(required = False,widget=forms.HiddenInput())
    captain.disabled=True

class ReservationTimeUnloggedForm(forms.Form):
    ''' Formulario de plazo de reserva para usuarios sin login: fecha inicio, fecha fin y un campo oculto para guardar la id de seguimiento '''
    start_date = forms.DateField(required=True,widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(required=True,widget=forms.DateInput(attrs={'type':'date'}))
    user = forms.CharField(widget=forms.HiddenInput())
    captain = forms.BooleanField(required = False,widget=forms.HiddenInput())
    captain.disabled=True



class EditProfileForm(forms.Form):
    ''' Formulario de edición de perfil '''
    name = forms.CharField(max_length=50, required=True, label="Nombre")
    surname = forms.CharField(max_length=100, required=True, label="Apellidos")
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    email = forms.EmailField(max_length=50, required=True, label="Correo electrónico")
    license_number = forms.CharField(
        max_length=50,
        required=False,
        label="Número de Licencia",
        help_text="Introduce el número de licencia si corresponde."
    )