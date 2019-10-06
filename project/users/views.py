from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import InvitationForm
from .models import User


# Create your views here.

@method_decorator(login_required, name='dispatch')
class UserDetailView(generic.DetailView):
    """
    View zur Detail Anzeige der Nutzerinformationen.
    """
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self):
        """
        Anpassung der get_object-Funktion zum automatischen Erhalten des aktuellen Nutzers
        """
        return self.request.user


@method_decorator(login_required, name='dispatch')
class UserUpdateView(generic.UpdateView):
    """
    View zur Bearbeitung des eigenen Nutzers.
    """
    model = User
    fields = ('avatar', 'username', 'first_name', 'last_name', 'email',)
    success_url = reverse_lazy('users:user-detail')
    template_name = 'users/user_update.html'

    def get_object(self):
        """
        Anpassung der get_object-Funktion zum automatischen Erhalten des aktuellen Nutzers
        """
        return self.request.user


@method_decorator(login_required, name='dispatch')
class UserDeleteView(generic.DeleteView):
    """
    View zum Löschen eines eigenen Nutzers.
    """
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:user-deleted')

    def get_object(self):
        """
        Anpassung der get_object-Funktion zum automatischen Erhalten des aktuellen Nutzers
        """
        return self.request.user


@login_required
def change_password(request):
    """
    Funktion zum Ändern des Passwortes.
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordChangeForm(request.user, request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data as required
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            # redirect to a new URL:
            return redirect('index')
        else:
            # return error messages and form
            messages.error(request, 'Please correct the error below.')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/user_password_update.html', {
        'form': form
    })


@login_required
def share_calendar(request):
    """
    Funktion um eine Freigabe und eine Invitation für einen User hinzuzufügen.
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvitationForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # get wished user by username
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()

            # add share and invitation if not already done
            if not user in request.user.shares.all():
                request.user.shares.add(user)
                request.user.invited.add(user)

            # remove invitation if add user with an invitation
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
    """
    Funktion um Freigabe und Invitation zu entfernen.
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvitationForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # get wished user by username
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()

            # remove user from share and remove invitation
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
    """
    Funktion um eine Invitation zu entfernen.
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvitationForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # get wished user by username
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()

            # remove invitation
            request.user.invitations.remove(user)
            # redirect to a new URL:
            return redirect(reverse_lazy('users:shares-detail'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InvitationForm()

    return render(request, 'users/shares_detail.html', {'form': form})
