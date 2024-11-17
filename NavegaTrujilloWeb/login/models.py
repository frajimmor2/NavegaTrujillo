from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, Group, Permission
from django.db import models

class User(AbstractBaseUser):
    #username = models.CharField(max_length=30, unique=True, null=True)
    email = models.EmailField(unique=True)
    #is_active = models.BooleanField(default=True) No se si nosotros lo añadimos
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    '''
    groups = models.ManyToManyField(
        Group,
        related_name="groups",  # Cambiamos el related_name
        blank=True,
        help_text="Los grupos a los que pertenece este usuario.",
        verbose_name="grupos",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions",  # Cambiamos el related_name
        blank=True,
        help_text="Permisos específicos asignados a este usuario.",
        verbose_name="permisos de usuario",
    )
    '''

    USERNAME_FIELD = 'email' 

    def __str__(self):
        return f"{self.email}"
            
class Administrator:
    def __init__(self, user: User):
        self.user = user
        self.user.is_staff = True  # Asignamos el rol de administrador

    def __str__(self):
        return f"{self.user.email}"

# Modelo de superusuario (composición)
class SuperUser:
    def __init__(self, user: User):
        self.user = user
        self.user.is_staff = True  # Asignamos el rol de administrador
        self.user.is_superuser = True  # Asignamos el rol de superusuario

    def __str__(self):
        return f"{self.user.email}"