from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .models import User

# Create your views here.

@method_decorator(login_required, name='dispatch')
class UserDetailView(generic.DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class UserSharesDetailView(generic.DetailView):
    model = User
    template_name = 'users/shares_detail.html'

    def get_object(self):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class UserUpdateView(generic.UpdateView):
    model = User
    fields = ('avatar', 'username', 'first_name', 'last_name', 'email',)
    success_url = reverse_lazy('users:user-detail')
    template_name = 'users/user_update.html'
    
    def get_object(self):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class UserSharesUpdateView(generic.UpdateView):
    model = User
    fields = ('shares',)
    success_url = reverse_lazy('users:shares-detail')
    template_name = 'users/shares_update.html'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(UserSharesUpdateView, self).get_form(form_class)
        form.fields["shares"].queryset = User.objects.exclude(pk=self.request.user.id).order_by('last_name')
        return form



@method_decorator(login_required, name='dispatch')
class UserDeleteView(generic.DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:user-deleted')

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