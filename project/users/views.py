from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from users.admin import UserCreationForm
from users.models import MyUser

# Create your views here.


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


@method_decorator(login_required, name='dispatch')
class MyUserDetailView(generic.DetailView):
    model = MyUser
    template_name = "users/detail.html"
    #context_object_name = 'datauser'

    def get_object(self):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class MyUserUpdateView(generic.UpdateView):
    model = MyUser
    fields = ('first_name', 'last_name', 'email',)
    success_url = reverse_lazy('userdetail')
    template_name = 'users/update.html'
    
    def get_object(self):
        return self.request.user


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })