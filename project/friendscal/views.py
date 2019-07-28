from django import forms
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.db.models import Q

from django.contrib.auth.mixins import UserPassesTestMixin

from django.conf import settings

from .models import Appointment

import datetime


# Create your views here.
def index(request):
    return HttpResponse("HELLO FROM FRIENDSCAL")


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


def events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    # user = request.GET.get('user')
    # if request.user.user_set.filter(pk=user) or request.user == user:
        # data = Appointment.objects.filter(user=user, end__range=(start, end)).values()          

    users = request.user.user_set.all()

    data = Appointment.objects.filter(Q(user__in=users) | Q(user=request.user), Q(end__range=(start, end)) | Q(start__range=(start, end))).values()

    data = [item for item in data]
    for counter, element in enumerate(data):
        data[counter]['id'] = str(element['uuid'])
        del data[counter]['uuid']
    #return JsonResponse(json.dumps(data, ensure_ascii=False), safe=False)
    return JsonResponse(data, safe=False)