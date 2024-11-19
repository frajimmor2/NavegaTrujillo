from django.http import HttpResponse
from django.shortcuts import render
from .models import Shopping_basket, Client
from django.utils import timezone


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
