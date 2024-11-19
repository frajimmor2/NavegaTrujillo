from django.http import HttpResponse
from django.shortcuts import render
from .models import Shopping_basket, Client
from django.utils import timezone


def home(request):
    return render(request,"./business/home_view.html")

def shopping_basket_view(request):
    print(request.user)
    if request.user.is_authenticated:
        if Shopping_basket.objects.filter(Shopping_basket.Client == request.user.client) == 0:

        #shopping_basket = Shopping_basket.objects.get_or_create(Client=request.user.client)
        #has_ships = shopping_basket.ships.exists() 
            newClient = Client(license_number = "", license_validated = False)
            request.user.client = newClient
            newShopping_basket = Shopping_basket(rental_start_date= timezone.now.date(),  rental_end_date= timezone.now.date(), captain_amount= 0)
            newShopping_basket.save()
            shopping_basket = newShopping_basket
            has_ships = shopping_basket.ships
        else:
            shopping_basket = Shopping_basket.objects.get(Shopping_basket.Client == request.user.client)
            has_ships = shopping_basket.ships
    else:

        return HttpResponse("Usuario no autenticado", status=401)
    
    return render(request, 'shopping_basket.html', {'shopping_basket': shopping_basket, 'has_ships': has_ships})
