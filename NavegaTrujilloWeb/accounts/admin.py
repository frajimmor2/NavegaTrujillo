from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("name","surname","email", "username", "password", "password")
    
    fieldsets = (
        (None, {'fields': ('name', 'surname', 'email', 'username', 'password1', 'password2')}),
    )

    add_fieldsets = (
        (None, {'fields': ('name', 'surname', 'email', 'username', 'password1', 'password2')}),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
