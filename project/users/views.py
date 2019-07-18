from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .admin import UserCreationForm
from .models import User

# Create your views here.


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/user_create.html'


@method_decorator(login_required, name='dispatch')
class UserDetailView(generic.DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class UserUpdateView(generic.UpdateView):
    model = User
    fields = ('avatar', 'first_name', 'last_name', 'email', 'share')
    success_url = reverse_lazy('users:detail')
    template_name = 'users/user_update.html'
    
    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(UserUpdateView, self).get_form(form_class)
        form.fields["share"].queryset = User.objects.exclude(pk=self.request.user.id)
        return form


@method_decorator(login_required, name='dispatch')
class UserDeleteView(generic.DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:deleted')

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
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/user_password_update.html', {
        'form': form
    })