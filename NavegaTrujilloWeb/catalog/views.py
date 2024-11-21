from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext
from business.models import Ship,Port, Shopping_basket
from .forms import ShipForm, shopping_basket_form

# Create your views here.

def list(request):


    ships = Ship.objects.all().order_by('capacity')

    return render(request,"./catalog/list.html",{"ships":ships})

def show(request, ship_id):
    if request.method=="GET":
        try: 
            ship = Ship.objects.get(id=ship_id)
        except:
            ship = False
        if not ship:
            return  render(request,"./business/home_view.html")

        form = ShipForm()
        form_shopping_basket = shopping_basket_form()
        #esta
        #print(request.user.client.shopping_basket.id)
        return render(request,"./catalog/show.html", {"ship":ship,"form":form})

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
        return  render(request,"./business/home_view.html")
    
    #form_shopping_basket = shopping_basket_form()

    form_shopping_basket = shopping_basket_form(request.POST)
    
    if form_shopping_basket.is_valid():
        print("Se esta ejecutando el codigo del form")
        shopping_basket, create = Shopping_basket.objects.get_or_create(client=request.user.client)
        ship = Ship.objects.get(id=ship_id)
        shopping_basket.ships.add(ship)
        shopping_basket.captain_amount = shopping_basket.captain_amount() + 1 if form_shopping_basket.captain else 0
        shopping_basket.save()
    try: 
        ship = Ship.objects.get(id=ship_id)
    except:
        ship = False
    if not ship:
        return  render(request,"./business/home_view.html")

   

    return render(request,"./catalog/show.html",{"ship":ship})
