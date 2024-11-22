from django.shortcuts import render,redirect
from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext
from business.models import Ship,Port
from .forms import ShipForm,ReservationForm

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
        form2 = ReservationForm()

        return render(request,"./catalog/show.html", {"ship":ship,"ship_form":form,"reservation_form":form2})

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

    ''' Esta función toma el formulario enviado desde la vista singular (o el home cuando se añada la opción),
    cambia el precio del barco si es necesario, y comienza el proceso de alquiler rápido (para usuario no logueado) '''

    if request.method=="POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["captain"]:
                print("Sí")
            else:
                print("No")
        try:
            ship = Ship.objects.get(id=ship_id)
        except:
            ship = False

        if not ship:
            ''' Esto nunca debería pasar, requiere usar herramientas externas y ser tonto a la vez '''
            return HttpResponse("¿Cómo has llegado aquí?",404)

        form = "formulario" # TODO añadir el formulario

        return render(request,"./catalog/reservation.html",{"ship_id":ship_id,"ship_name":ship.name,"form":form})

    else:
        ''' Solo pasa si se entra poniendo la url en el buscador directamente '''
        return HttpResponse("Por favor, accede desde el escaparate o la página del barco que quieras reservar",405)



