from django.http import HttpResponse
from django.shortcuts import render
from .models import Client, Shopping_basket


def home(request):
    return render(request,"./business/home_view.html")

def shopping_basket_view(request):
    if request.user.is_authenticated:
        #cliente = Client.objects.get(user=request.user)
        shopping_basket = Shopping_basket.objects.get_or_create(Client=request.user.client)
        has_ships = shopping_basket.ships.exists() 
    else:
        return HttpResponse("Usuario no autenticado", status=401)

    return render(request, 'shopping_basket.html', {'shopping_basket': shopping_basket, 'has_ships': has_ships})
