from django.http import HttpResponse
from django.shortcuts import render
from .models import Shopping_basket, Client, Ship
from django.utils import timezone
from .forms import ReservationTimeForm
from catalog.forms import ReservationForm


def home(request):
    return render(request,"./business/home_view.html")

def cart(request):
    print(request.user)
    print(dir(request))
    if request.user.is_authenticated:
        print(Shopping_basket.client)
        print("user ahora")
        print(request.user.client)
        
        shopping_basket, created = Shopping_basket.objects.get_or_create(client=request.user.client)
        print(shopping_basket)
        if shopping_basket.ships.exists():
            has_ships = shopping_basket.ships.exists() 
            print(has_ships)
        else:
            has_ships = False
    else:
        return HttpResponse("Usuario no autenticado", status=401)
    
    return render(request, './business/cart.html', {'shopping_basket': shopping_basket, 'has_ships': has_ships})

def reservation(request,ship_id):
    ''' Punto de toma de los datos de la reserva (plazo en el que se va a reservar, y método de pago (contrareembolso por ahora)'''
    try:
        ship = Ship.objects.get(id=ship_id)
    except:
        ship = False

    if not ship:
        ''' No debería pasar sin herramientas externas, este endpoint solo recibe Posts '''
        return HttpResponse("Ese barco no existe; ¿como has llegado aquí?", status=404)
     
    form = ReservationForm(request.POST)
    if form.is_valid():
        captain = form.cleaned_data["captain"]
    else :
        ''' Tampoco debería pasar, el formulario es un solo booleano '''
        return HttpResponse("Algo ha ido mal, vuelve a intentarlo", status=500)

    ''' El formulario anterior ya no hace falta, reescribo '''
    form = ReservationTimeForm()

    # TODO crear lista con los intervalos en los que el barco ya está reservado
    taken_days = []

    return render(request, './business/reservation.html', {'form': form,'taken_days': taken_days }) 






