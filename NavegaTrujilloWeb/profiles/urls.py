from django.contrib import admin
from django.urls import path, include

from profiles.views import CustomLoginView

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('', include('profiles.urls')),  # Asegúrate de que este "include" esté correcto
    path('login/', CustomLoginView.as_view(), name='login'),
]
