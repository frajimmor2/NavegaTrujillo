from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext
from business.models import Ship,Port
from .forms import ShipForm,ReservationForm

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
        form2 = ReservationForm()

        return render(request,"./catalog/show.html", {"ship":ship,"ship_form":form,"reservation_form":form2})

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

def reservation(request, ship_id):
    if request.method=="POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["captain"]:
                print("Sí")
            else:
                print("No")
        return render(request,"./catalog/reservation.html")
    else:
        pass
