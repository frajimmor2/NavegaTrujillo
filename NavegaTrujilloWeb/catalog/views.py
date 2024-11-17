from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext
from business.models import Ship,Port
from .forms import ShipForm

# Create your views here.

def list(request):


    ships = Ship.objects.all()

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


    return render(request,"./catalog/show.html",{"ship":ship})
