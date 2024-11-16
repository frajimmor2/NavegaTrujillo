from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import EmailAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Cambia al nombre de tu plantilla
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')  # Redirige a una vista tras el login
