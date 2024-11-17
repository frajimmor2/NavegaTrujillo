from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# Personalización del modelo User en el admin
class UserAdmin(DefaultUserAdmin):
    model = User
    # Campos a mostrar en la lista de usuarios
    list_display = ('email', 'is_staff', 'is_superuser')
    # Campos a usar para la búsqueda en el admin
    search_fields = ('email',)
    # Campos para filtrado
    list_filter = ('is_staff', 'is_superuser')
    # Campos para la creación y modificación de usuarios
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

# Registrar el modelo User con la clase de administración personalizada
admin.site.register(User, UserAdmin)
