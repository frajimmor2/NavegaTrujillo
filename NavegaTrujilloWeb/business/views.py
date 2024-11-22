from django.shortcuts import render, redirect
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Port

def home(request):
    return render(request,"./business/home_view.html")



@login_required
def add_port(request):
    # Verifica si el usuario tiene permiso de staff
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == "POST":
        ubication = request.POST.get("ubication")
        if ubication:
            Port.objects.create(ubication=ubication)
            return redirect("home")  # Redirige al usuario al inicio después de añadir el puerto

    return render(request, "./business/add_port.html")

