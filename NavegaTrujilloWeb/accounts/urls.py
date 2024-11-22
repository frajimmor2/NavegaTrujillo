from django.urls import path

from .views import SignUpView,LoginView,FastLoginView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("fast_login/<int:ship_id>",FastLoginView.as_view(), name="fast_login"),
]
