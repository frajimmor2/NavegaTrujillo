from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField, UserModel
from django.contrib.auth import forms,authenticate,login
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username","name","surname","email")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username","name","surname","email")


class LoginForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
            """
            The 'request' parameter is set for custom auth use by subclasses.
            The form data comes in via the standard 'data' kwarg.
            """
            self.request = request
            self.user_cache = None
            super().__init__(*args, **kwargs)

            self.error_messages = {
                    "invalid_login": (
                        "Por favor, introduzca un email y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas."
                    ),
                    "inactive": ("This account is inactive."),
                }

            # Set the max length and label for the "username" field.
            self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
            username_max_length = self.username_field.max_length or 254
            self.fields["username"].max_length = username_max_length
            self.fields["username"].widget.attrs["maxlength"] = username_max_length
            self.fields["username"].label = "Tu email"

    def clean(self):
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")

            if username is not None and password:
                try:
                    c = CustomUser.objects.get(email=username)
                except:
                    c = False
                if c:
                    self.cleaned_data["username"] = c.username
                    self.user_cache = authenticate(
                        self.request, username=c.username, password=password
                    )
                else:
                    raise self.get_invalid_login_error()
                if self.user_cache is None:
                    raise self.get_invalid_login_error()
                else:
                    self.confirm_login_allowed(self.user_cache)
            return self.cleaned_data






