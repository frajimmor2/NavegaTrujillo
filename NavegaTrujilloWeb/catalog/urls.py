from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.list, name="list"),
    path('catalog/ship/<int:ship_id>/',views.show, name="show"),
    path('catalog/ship/<int:ship_id>/reserva',views.reservation, name="reservation"),
    path('catalog/results/', views.filtered_list, name="filter"),
    path('edit/<int:ship_id>/', views.edit_ship, name='edit_ship'),
    path('delete/<int:ship_id>/', views.delete_ship, name='delete_ship'),
]
