from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django import forms

from .models import User
from .forms import InvitationForm

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


@login_required
def share_calendar(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvitationForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()

            request.user.shares.add(user)
            request.user.invited.add(user)

            if user in request.user.invitations.all():
                request.user.invitations.remove(user)
            # redirect to a new URL:
            return redirect(reverse_lazy('users:shares-detail'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InvitationForm()

    return render(request, 'users/shares_detail.html', {'form': form})


@login_required
def unshare_calendar(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvitationForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()

            request.user.shares.remove(user)
            request.user.invited.remove(user)
            # redirect to a new URL:
            return redirect(reverse_lazy('users:shares-detail'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InvitationForm()

    return render(request, 'users/shares_detail.html', {'form': form})


@login_required
def remove_invitation(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvitationForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()

            request.user.invitations.remove(user)
            # redirect to a new URL:
            return redirect(reverse_lazy('users:shares-detail'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InvitationForm()

    return render(request, 'users/shares_detail.html', {'form': form})