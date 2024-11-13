from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse

def home(request):

    content = open("../NavegaTrujilloWeb/business/view_templates/home_view.html")
    tplt = Template(content.read())
    content.close()

    ctx = Context()
    view = tplt.render(ctx)

    return HttpResponse(view)
