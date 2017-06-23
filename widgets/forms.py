from django.contrib.auth.forms import UserCreationForm

from widgets.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'zip_code', 'gender']
