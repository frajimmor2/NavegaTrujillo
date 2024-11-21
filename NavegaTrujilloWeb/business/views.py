import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Ship, Shopping_basket, Client
from django.utils import timezone


def home(request):
    return render(request,"./business/home_view.html")


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        if not cart:
            print("El carrito está vacío, inicializando...")
            ships = Ship.objects.all()
            cart = {ship.id: {"quantity": 0} for ship in ships}
        
        
    except:
        cart = {}
    
    
    '''ships_dict = {}
    for ship in Ship.objects.all():
        print(ship.id)
        ships_dict[ship.id] = {"quantity": 1}
    
        
    cart = ships_dict'''
        
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    
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



