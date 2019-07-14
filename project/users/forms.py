from django import forms
from .models import User

class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)