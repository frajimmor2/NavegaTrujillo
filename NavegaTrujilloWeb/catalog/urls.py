from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.list, name="list"),
    path('catalog/ship/<int:ship_id>/',views.show, name="show"),
]
