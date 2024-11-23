from django.shortcuts import render,redirect
from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext
from business.models import Ship,Port
from .forms import ShipForm,ReservationForm,ReservationFormNotLogged,ReservationDataForm

# Create your views here.

def list(request):
    ''' Lista, básico de entender, hay que mover esta función para que aplique también al escaparate en home'''

    ships = Ship.objects.all()

    return render(request,"./catalog/list.html",{"ships":ships})

def show(request, ship_id):

    ''' En caso de ser un get, toma el barco (si no existe redirige a home), añade los formularios pertinentes (reserva y cambio de datos)
        y lo manda al frontend; Recibe el POST de cambio de datos también, el cuál aplica al barco (siempre vendrá de un administrador)'''

    if request.method=="GET":
        try: 
            ship = Ship.objects.get(id=ship_id)
        except:
            ship = False
        if not ship:
            return redirect("/",permanent=True)

        form = ShipForm()
        if (request.user.is_authenticated and request.user.client.license_validated) or not ship.need_license:
            reservation_form = ReservationForm()
        else:
            reservation_form = ReservationFormNotLogged()

        return render(request,"./catalog/show.html", {"ship":ship,"ship_form":form,"reservation_form":reservation_form})

    form = ShipForm(request.POST)
    if form.is_valid():
        ship = Ship.objects.get(id=ship_id)
        ship.capacity = form.cleaned_data["capacity"]
        ship.needs_license = form.cleaned_data["needs_license"]
        ship.rent_per_day = form.cleaned_data["rent_per_day"]
        ship.available = form.cleaned_data["available"]
        ship.description = form.cleaned_data["description"]
        ship.save() 
    try: 
        ship = Ship.objects.get(id=ship_id)
    except:
        ship = False

    if not ship:
        return redirect("/",permanent=True)

    return render(request,"./catalog/show.html",{"ship":ship})


def reservation(request, ship_id):

    ''' Esta función se accede desde la vista singular (o el home cuando se añada la opción),
        y comienza el proceso de alquiler rápido (para usuario no logueado) '''
    try:
        ship = Ship.objects.get(id=ship_id)
    except:
        ship = False

    if not ship:
        ''' Esto solo pasa si se accede escribiendo una url incorrecta directamente '''
        return HttpResponse("Ese barco no existe",404)

    form = ReservationDataForm() 

    return render(request,"./catalog/reservation.html",{"ship_id":ship_id,"ship_name":ship.name,"form":form})


