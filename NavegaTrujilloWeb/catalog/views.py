from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse


# Create your views here.

def list(request):

    with open("./catalog/view_templates/list.html") as content:
        tplt = Template(content.read())

    ctx = Context()
    view = tplt.render(ctx)

    return HttpResponse(view)
