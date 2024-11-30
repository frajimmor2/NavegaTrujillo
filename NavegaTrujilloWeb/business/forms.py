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