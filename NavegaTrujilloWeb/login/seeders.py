
from NavegaTrujilloWeb.login.models import CustomUser

# Crea un usuario de prueba con email y contraseña
user = CustomUser.objects.create_user(email='testuser@example.com', password='password123')

# Guarda el usuario
user.save()