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
        #print("sisi")
        
    except:
        cart = {}
        #print("adios")


    print('Cart bro:', cart)


    json.dumps({            # AQUI SE AÑADE EL VALOR MANUALMENTE DE LA COOKIE
            1: 5,
    })


    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        
        try:
            cartItems += cart[i]["quantity"]
            ship = Ship.objects.get(id=i)
            print(ship)
            total = (ship.rent_per_day * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            
            items.append({'ship': ship, 'quantity':cart[i]["quantity"],'get_total':total})

        except:
            pass

        print(items)
    return {"items": items, "order": order, "cartItems": cartItems}

def cart(request):
    #print(dir(request.session))
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
    #print(cookieCart(request))
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
    return render(request, './business/cart.html', {
    'cartItems':cartItems ,'order':order, 'items':items#, 'shopping_basket': shopping_basket, 'has_ships': has_ships
    })



