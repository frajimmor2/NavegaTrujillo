from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
from business.models import Ship,Port

# Create your views here.

def list(request):

    with open("./catalog/view_templates/list.html") as content:
        tplt = Template(content.read())

    ships = Ship.objects.all()
    ctx = Context({'ships':ships})
    view = tplt.render(ctx)

    return HttpResponse(view)

def show(request, ship_id):
    try: 
        ship = Ship.objects.get(id=ship_id)
        port = Port.objects.get(id=ship.port_id)
    except:
        ship = False
        port = False

    if ship:
        with open("./catalog/view_templates/show.html") as content:
            tplt = Template(content.read())
    else:
        with open("./business/view_templates/home_view.html") as content:
            tplt = Template(content.read())
    
    ctx = Context({'ship':ship,'port':port.ubication})
    view = tplt.render(ctx)

    return HttpResponse(view)
