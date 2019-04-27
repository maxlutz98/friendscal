from django.shortcuts import render

# Create your views here.

from django.urls import reverse_lazy
from django.views import generic

from users.models import MyUser

from users.admin import UserCreationForm, UserChangeForm, UserChangePassword

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

class MyUserDetailView(generic.DetailView):
    model = MyUser
    template_name = "users/detail.html"
    context_object_name = 'user'

class MyUserUpdateView(generic.UpdateView):
    form_class = UserChangeForm
    model = MyUser
    success_url = reverse_lazy('login')
    template_name = 'users/update.html'

class MyUserPWUpdateView(generic.UpdateView):
    form_class = UserChangePassword
    model = MyUser
    success_url = reverse_lazy('login')
    template_name = 'users/pw_update.html'



# TODO: show and change