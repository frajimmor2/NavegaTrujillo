from django.urls import path,include

from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),
    path('reserva/<int:ship_id>', views.reservation, name="reservation_dates"),
    path('reserva/<int:ship_id>/confirmacion', views.confirm_reservation, name="confirm_reservation"),
    path('paypal/<int:ship_id>/confirmacion/<int:captain>', views.confirm_reservation_paypal, name="confirm_reservation_paypal"),
    path('cart/', views.cart, name="cart"),
    path('cart/reserva', views.cart_reservation, name = "cart_reservation"),
    path('cart/reserva/confirmacion', views.confirm_reservation_cart, name = "cart_reservation_confirm"),
    path('add-port/', views.add_port, name="add_port"),
    path('add-ship/', views.add_ship, name="add_ship"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('accounts/<str:username>/', views.manage_license, name="manage_license"),
    #path('paypal_confirm',views.paypal_congrats,name="paypal_congrats"),
    path('accounts/', views.user_management, name="user_management"),
    path('cart/reserva/paypal',views.paypal_cart, name="paypal_cart"),
    path('cart/reserva/paypal/confirmacion/<int:lookup_id>',views.paypal_cart_confirmation,name="paypal_cart_confirmation"),
    path('reservations/', views.list_reservations_admin, name="list_reservations_admin"),
    path('update-reservation/<int:reservation_id>/', views.update_reservation_state, name='update_reservation_state'),
    path('track-reservation/', views.track_reservation, name='track_reservation'),
    path('my-reservations/', views.my_reservations, name="my_reservations"),
    path('my-reservations/<int:reservation_id>', views.my_reservation_status_view, name="reservation_view"),
    path('cancel-reservation/<int:reservation_id>', views.cancel_reservation, name="cancel_reservation"),
    path('cancel-reservation/lookup/<int:reservation_id>', views.cancel_reservation_lookup, name='cancel_reservation_lookup'),
    path('my-reservations/<int:reservation_id>/pay', views.pay_reservation, name='pay_reservation'),
]
