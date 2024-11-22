from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),
    path('add-port/', views.add_port, name="add_port"),
]