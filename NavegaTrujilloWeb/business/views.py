from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse

def home(request):
    return render(request,"./business/home_view.html")
