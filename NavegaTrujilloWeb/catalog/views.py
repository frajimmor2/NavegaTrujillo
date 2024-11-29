from django.shortcuts import render,redirect
from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext
from .forms import ShipForm,ReservationForm,ReservationFormNotLogged,ReservationDataForm,shopping_basket_form
from business.models import Ship,Port, Shopping_basket
from .forms import ShipForm, shopping_basket_form, dates_form
from catalog.filters import ship_filter
# Create your views here.

def list(request):
    ''' Lista, básico de entender, hay que mover esta función para que aplique también al escaparate en home'''

    ships = Ship.objects.all().order_by('capacity')
    
    f = ship_filter(request.GET, queryset=(ships))
    form = dates_form()
    return render(request,"./catalog/list.html",{"ships":ships, "filter": f, "form": form})

def filtered_list(request):
    ships = Ship.objects.all().order_by('capacity')
    #Ship.objects.all().order_by('capacity')
    '''Es un get que recoge lo del formulario y filtra según él, en caso de dar error pues la lista de barcos esta vacia'''
    #form = search_form()

    
    ''' JesuCristo perdóname por lo que estoy a punto de hacer'''

    f = ship_filter(request.GET, queryset=(ships))
    ships = f.qs

    '''Ahora se viene el codigo de la cabra, con unos ifs miro que el tema fechas esta bien, meto el codigo de comprobar si un barco esta disp
    en las fechas dadas y si no lo está le cambio el disp a no disp sin guardarlo en la bd'''
    form = dates_form()
    


    return render(request,"./catalog/list.html" ,{"ships":ships, "filter": f, "form": form})

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
        form_shopping_basket = shopping_basket_form()
        return render(request,"./catalog/show.html", {"ship":ship,"form":form,"form_shopping_basket":form_shopping_basket,"reservation_form":reservation_form})

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
    

    form_shopping_basket = shopping_basket_form(request.POST)
    
    if form_shopping_basket.is_valid():
        print("Se esta ejecutando el codigo del form")
        shopping_basket, create = Shopping_basket.objects.get_or_create(client=request.user.client)
        ship = Ship.objects.get(id=ship_id)
        shopping_basket.ships.add(ship)
        shopping_basket.captain_amount = shopping_basket.captain_amount() + 1 if form_shopping_basket.captain else 0
        shopping_basket.save()

    form = ShipForm()
    reservation_form = ReservationFormNotLogged()
    form_shopping_basket = form_shopping_basket()

    return render(request,"./catalog/show.html",{"ship":ship,"form_shopping_basket":form_shopping_basket,"reservation_form":reservation_form,"form":form})


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


