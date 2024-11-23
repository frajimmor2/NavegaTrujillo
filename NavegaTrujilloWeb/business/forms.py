from django import forms

class ReservationTimeForm(forms.Form):
    ''' Formulario de plazo de reserva: fecha inicio y fecha fin '''
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)

class ReservationTimeUnloggedForm(forms.Form):
    ''' Formulario de plazo de reserva para usuarios sin login: fecha inicio, fecha fin y un campo oculto para guardar la id de seguimiento '''
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
    user = forms.CharField(widget=forms.HiddenInput())


