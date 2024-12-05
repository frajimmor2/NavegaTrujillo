from django.shortcuts import render,redirect
from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext
from .forms import ShipForm,ReservationForm,ReservationFormNotLogged,ReservationDataForm,shopping_basket_form,ReservationDataHiddenForm
from business.models import Ship,Port, Shopping_basket
from .forms import ShipForm, shopping_basket_form, dates_form
from catalog.filters import ship_filter
from datetime import timedelta, date, datetime
from django.urls import reverse,reverse_lazy
from paypal.standard.forms import PayPalPaymentsForm
import json


# Create your views here.

def list(request):
    ''' Lista, básico de entender, hay que mover esta función para que aplique también al escaparate en home'''

    ships = Ship.objects.all().order_by('capacity')
    
    f = ship_filter(request.GET, queryset=(ships))
    form = dates_form()
    form_obligatory_captain = ReservationFormNotLogged()
    form_optional_captain = ReservationForm()
    return render(request,"./catalog/list.html",{"ships":ships, "filter": f, "form": form,"form_obligatory_captain":form_obligatory_captain,"form_optional_captain":form_optional_captain})

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
    form = dates_form(request.GET)
    if form.is_valid():
        start = datetime.strptime(request.GET.get('rent_start_day'), "%Y-%m-%d").date() if request.GET.get('rent_start_day') else date(1900, 12, 25)
        end = datetime.strptime(request.GET.get('rent_end_day'), "%Y-%m-%d").date() if request.GET.get('rent_end_day') else date(1900, 12, 25)

        rent_days = set()
        delta_rent_days = end-start
        delta_rent_days = delta_rent_days.days
        rent_days.add(start)

        for i in range(delta_rent_days):
            rent_days.add(start+timedelta(days=i))
        

        for ship in ships:
            taken_days = set()
            for reservation in ship.reservation_set.all():
                start_date = reservation.rental_start_date
                end_date = reservation.rental_end_date
                
                if start_date in taken_days and end_date in taken_days:
                    break
                delta = end_date-start_date
                delta = delta.days
                
                taken_days.add(start_date)
                for i in range(delta):
                    taken_days.add(start_date+timedelta(days=i))
                
                
                for day in rent_days:
                    if day in taken_days:
                        ship.available = False

        ships_f = Ship.objects.all().order_by('capacity')

        for ship in ships_f:
            if not(ship in ships):
                ship.available= False    
                
    form_obligatory_captain = ReservationFormNotLogged()
    form_optional_captain = ReservationForm()
        


    return render(request,"./catalog/list.html" ,{"ships":ships_f, "filter": f, "form": form,"form_obligatory_captain":form_obligatory_captain,"form_optional_captain":form_optional_captain})

def show(request, ship_id):

    ''' En caso de ser un get, toma el barco (si no existe redirige a home), añade los formularios pertinentes (reserva y cambio de datos)
        y lo manda al frontend; Recibe el POST de cambio de datos también, el cuál aplica al barco (siempre vendrá de un administrador)'''

    shipInCart = False
    cart = json.loads(request.COOKIES['cart'])
    if str(ship_id) in cart.keys():
        shipInCart = True

    cartItems = 0
    items = []
    for i in cart:
    
        try:
            cartItems += cart[i]["quantity"]
            ship = Ship.objects.get(id=i)            
            items.append({'ship': ship, 'quantity':cart[i]["quantity"]})

        except:
            pass

    current_ship = Ship.objects.get(id=ship_id)
    item = next((item for item in items if item['ship'] == current_ship), None)

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

        return render(request,"./catalog/show.html", {"ship":ship,"ship_form":form,"reservation_form":reservation_form, "shipInCart":shipInCart, "item":item})

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
        shopping_basket, create = Shopping_basket.objects.get_or_create(client=request.user.client)
        ship = Ship.objects.get(id=ship_id)
        shopping_basket.ships.add(ship)
        shopping_basket.captain_amount = shopping_basket.captain_amount() + 1 if form_shopping_basket.captain else 0
        shopping_basket.save()

    form = ShipForm()
    reservation_form = ReservationFormNotLogged()
    form_shopping_basket = form_shopping_basket()

    return render(request,"./catalog/show.html",{"ship":ship,"form_shopping_basket":form_shopping_basket,"reservation_form":reservation_form,"form":form, "shipInCart":shipInCart, "item":item})


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
    form = ReservationForm(request.POST)

    if ((request.user.is_authenticated and request.user.client.license_validated) or not ship.need_license) and form.is_valid():
        captain = form.cleaned_data['captain']
    else:
        form = ReservationFormNotLogged(request.POST)
        if form.is_valid():
            captain = form.cleaned_data['captain']
        else:
            captain = False

    form = ReservationDataForm() 
    form2 = ReservationDataHiddenForm()
    form2.initial['captain'] = captain
    form.initial['captain'] = captain

    
    paypal_dict = {
            "business": "sb-iqwdg34506520@business.example.com",
            "amount": str(ship.rent_per_day+[0,120][captain]+20) if ship.rent_per_day+[0,120][captain]<1000 else str(ship.rent_per_day+[0,120][captain]),
            "item_name": str(ship.name),
            "invoice": "",
            #"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),#request.build_absolute_uri(reverse("paypal_congrats")), # TODO create reservation registerer
            "return": request.build_absolute_uri(reverse_lazy("confirm_reservation_paypal",kwargs={'ship_id':ship_id,'captain':[0,1][captain]})), # TODO create view
            "cancel_return": request.build_absolute_uri(reverse('home')),
        }
    form_paypal = PayPalPaymentsForm(initial=paypal_dict)

    return render(request,"./catalog/reservation.html",{"ship_id":ship_id,"ship_name":ship.name,"form":form,"form_paypal":form_paypal,"form2":form2})

