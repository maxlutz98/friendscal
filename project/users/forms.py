from django import forms
from django_registration.forms import RegistrationForm

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'avatar')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('avatar', 'username', 'email', 'first_name', 'last_name', 'shares')


class MyCustomUserForm(RegistrationForm):
    """
    Anpasung des RegistrationForm:
    Formular zur Registrierung neuer Nutzer (CustomUser). Beinhaltet alle notwenigen Felder.
    """

    class Meta(RegistrationForm.Meta):
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'email',)


class InvitationForm(forms.Form):
    """
    Formular zum Bearbeiten von Freigaben.
    """
    username = forms.CharField(label='Nutzername', max_length=150,
                               help_text='Nutzername des Nutzers, welchem du eine Freigabe erteilen möchtest.')

    def __init__(self, *args, **kwargs):
        """
        Anpassung der __init__-Funktion zur zusätzlichen Übergabe der Anfrage.
        """
        self.request = kwargs.pop('request', None)
        super(InvitationForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Anpassung der clean-Funktion zum Überprüfen des eingegeben Nutzernamens und Hinzufügen entsprechender Fehlermeldungen.
        """
        cd = self.cleaned_data
        user = User.objects.filter(username=cd.get('username')).first()
        if not user:
            # Kein Nutzer
            self.add_error('username', "Nutzername existiert nicht.")
        elif user == self.request.user:
            # eigener Nutzer (Anfragesteller)
            self.add_error('username', "Es ist nicht möglich sich selbst eine Freigabe zu erteilen.")
        return cd
