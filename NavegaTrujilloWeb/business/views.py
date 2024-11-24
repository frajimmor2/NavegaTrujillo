import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Ship, Port, Shopping_basket, Client
from django.utils import timezone
from datetime import datetime


def home(request):

    ships = Ship.objects.all()[:8]
    ports = Port.objects.all()
    context = {"ships": ships, "ports": ports}
    return render(request,"./business/home_view.html", context)


def cookieCart(request):
    try:
        cart = {}
        cart = json.loads(request.COOKIES['cart'])
  
    except:
        cart = {}
    
    
    '''ships_dict = {}
    for ship in Ship.objects.all():
        print(ship.id)
        ships_dict[ship.id] = {"quantity": 1}
    
        
    cart = ships_dict'''
        
    print(cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False, 'captain_amount': 0, 'captain_cost': 0, 'total_with_captain': 0}
    cartItems = order['get_cart_items']

    rental_start_date = request.GET.get('rental_start_date', None)
    rental_end_date = request.GET.get('rental_end_date', None)
    rental_days = 0

    # Este if calcula los dias alquilados y si no esta especificado el rango de fechas, se pone por default 1 dia
    if rental_start_date and rental_end_date:
            rental_days = (datetime.strptime(rental_end_date, "%Y-%m-%d") - datetime.strptime(rental_start_date, "%Y-%m-%d")).days
            rental_days = max(1, rental_days)  # Hace que el mínimo de días sea 1
    else:
        rental_days = 1
    
    for i in cart:
        
        try:
            cartItems += cart[i]["quantity"]
            ship = Ship.objects.get(id=i)
            total = (ship.rent_per_day * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            
            items.append({'ship': ship, 'quantity':cart[i]["quantity"],'get_total':total})

        except:
            pass

    captain_amount = cart.get('captain_amount', 0)
    if captain_amount > cartItems:  # Este if es el que limita la cantidad de capitanes a la cantidad de barcos
        captain_amount = cartItems  

    order['captain_amount'] = captain_amount
    order['captain_cost'] = captain_amount * 120 * rental_days # Aqui guarda el precio de los capitanes para invocarlo usando order['coste_capitan']
    order['total_with_captain'] = order['get_cart_total'] + order['captain_cost']

    return {"items": items, "order": order, "cartItems": cartItems, "ships": Ship.objects.all()}

def cart(request):
    '''
    if request.user.is_authenticated:      
        shopping_basket, created = Shopping_basket.objects.get_or_create(customuser=request.user)
        has_ships = shopping_basket.ships.exists()

        return render(request, './business/cart.html', {
        'shopping_basket': shopping_basket,
        'has_ships': has_ships
    })
    
    else:
    '''
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
    return render(request, './business/cart.html', {
    'cartItems':cartItems ,'order':order, 'items':items  #, 'shopping_basket': shopping_basket, 'has_ships': has_ships
    })



