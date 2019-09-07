from django import forms
from django_registration.forms import RegistrationForm

from .models import User

class MyCustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'email',)


class InvitationForm(forms.Form):
    username = forms.CharField(label='Nutzername', max_length=150, help_text='Nutzername des Nutzers, welchem du eine Freigabe erteilen möchtest.')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InvitationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        user = User.objects.filter(username=cd.get('username')).first()
        if not user:
            self.add_error('username', "Nutzername existiert nicht.")
        elif user == self.request.user:
            self.add_error('username', "Es ist nicht möglich sich selbst eine Freigabe zu erteilen.")
        return cd

