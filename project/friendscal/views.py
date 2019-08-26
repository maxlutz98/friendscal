from django import forms
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.db.models import Q

from django.contrib.auth.mixins import UserPassesTestMixin

from django.conf import settings

from .models import Appointment

from users.models import User

import datetime


# Create your views here.

@method_decorator(login_required, name="dispatch")
class AppointmentCreateView(generic.CreateView):
    model = Appointment
    fields = ("title", "start", "end", "description", "location")
    success_url = reverse_lazy("friendscal:index")
    template_name = "friendscal/appointment_create.html"

    def get_form(self, form_class=None):
        form = super(AppointmentCreateView, self).get_form(form_class)
        form.fields['start'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields['end'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields["start"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M', date_attrs={"class": "datepicker"}, time_attrs={"class": "timepicker"})
        form.fields["end"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M', date_attrs={"class": "datepicker"}, time_attrs={"class": "timepicker"})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.cleaned_data['end'] < form.cleaned_data['start']:
            raise forms.ValidationError("End date must be later than start date")
        return super(AppointmentCreateView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class AppointmentDetailView(generic.DetailView):
    model = Appointment
    template_name = "friendscal/appointment_detail.html"


@method_decorator(login_required, name="dispatch")
class AppointmentUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Appointment
    fields = ("title", "start", "end", "description", "location")
    success_url = reverse_lazy("friendscal:index")
    template_name = "friendscal/appointment_update.html"

    def test_func(self):
        return self.request.user == Appointment.objects.get(pk=self.kwargs['pk']).user

    def get_form(self, form_class=None):
        form = super(AppointmentUpdateView, self).get_form(form_class)
        form.fields['start'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields['end'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields["start"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M', date_attrs={"class": "datepicker"}, time_attrs={"class": "timepicker"})
        form.fields["end"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M', date_attrs={"class": "datepicker"}, time_attrs={"class": "timepicker"})
        return form

    def form_valid(self, form):
        if form.cleaned_data['end'] < form.cleaned_data['start']:
            raise forms.ValidationError("End date must be later than start date")
        return super(AppointmentUpdateView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class AppointmentDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Appointment
    success_url = reverse_lazy("friendscal:index")

    def test_func(self):
        return self.request.user == Appointment.objects.get(pk=self.kwargs['pk']).user


@method_decorator(login_required, name="dispatch")
class AppointmentListView(generic.ListView):
    model = Appointment

    def get_queryset(self):
        # queryset = Appointment.objects.filter(user=self.request.user).filter(end__gte=datetime.datetime.today()).order_by('start')
        queryset = self.request.user.appointment_set.all().filter(end__gte=datetime.datetime.today()).order_by('start')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(AppointmentListView, self).get_context_data(*args, **kwargs)
        context["past_list"] = self.request.user.appointment_set.all().filter(end__range=(datetime.datetime.today() - datetime.timedelta(days=730), datetime.datetime.today())).order_by('-end')
        return context


@login_required
def events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    user = request.GET.get('user')
    first, last = user.split('_')
    user = User.objects.get(first_name=first, last_name=last)
    if user in request.user.user_set.all() or request.user == user:
        data = Appointment.objects.filter(Q(user=user), Q(end__range=(start, end)) | Q(start__range=(start, end)) | (Q(start__lte=start) & Q(end__gte=end))).values()
    else:
        data = []

    data = [item for item in data]
    for counter, element in enumerate(data):
        data[counter]['id'] = str(element['uuid'])
        del data[counter]['uuid']
    return JsonResponse(data, safe=False)


@login_required
def AppointmentJson(request, uuid):
    appointment = Appointment.objects.get(pk=uuid)
    
    data = {
        'uuid': str(appointment.uuid),
        'title': appointment.title,
        'start': '{dt:%d.%m.%Y %H:%M}'.format(dt=appointment.start),
        'end': '{dt:%d.%m.%Y %H:%M}'.format(dt=appointment.end),
        'description': appointment.description,
        'location': appointment.location,
        'user': appointment.user.get_full_name()
        }

    if request.user == appointment.user:
        data['can_edit'] = True

    return JsonResponse(data)


@login_required
def SessionAdd(request):
    name = request.POST.get("checked", "")
    
    first, last = name.split('_')
    user = User.objects.get(first_name=first, last_name=last)
    if user in request.user.user_set.all() or request.user == user:
        if not "checked" in request.session.keys():
            thislist = []
            thislist.append(name)
            request.session["checked"] = thislist
        else:
            if not name in request.session["checked"]:
                thislist = request.session["checked"]
                thislist.append(name)
                request.session["checked"] = thislist
    print(request.session["checked"])
    return JsonResponse({})


@login_required
def SessionRemove(request):
    name = request.POST.get("checked", "")

    if "checked" in request.session.keys():
        if name in request.session["checked"]:
            thislist = request.session["checked"]
            thislist.remove(name)
            request.session["checked"] = thislist
    print(request.session["checked"])
    return JsonResponse({})

