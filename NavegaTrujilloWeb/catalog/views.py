from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
from business.models import Ship

# Create your views here.

def list(request):

    with open("./catalog/view_templates/list.html") as content:
        tplt = Template(content.read())

    ships = Ship.objects.all()
    ctx = Context({'ships':ships})
    view = tplt.render(ctx)

    return HttpResponse(view)
