from django_registration.forms import RegistrationForm
from .models import User

class MyCustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'email',)