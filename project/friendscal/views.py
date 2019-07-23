from django import forms
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .models import Appointment

import datetime

# Create your views here.
def index(request):
    return HttpResponse("HELLO FROM FRIENDSCAL")


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    fields = ("title", "start", "end", "description", "location")
    success_url = reverse_lazy("friendscal:index")
    template_name = "friendscal/appointment_create.html"

    def get_form(self, form_class=None):
        form = super(AppointmentCreateView, self).get_form(form_class)
        form.fields["start"].widget.attrs.update({"class": "datepicker"})
        # form.fields['start'].widget.attrs.update(input_format='%d.%m.%Y')
        form.fields["end"].widget.attrs.update({"class": "datepicker"})
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
class AppointmentUpdateView(generic.UpdateView):
    model = Appointment
    fields = ("title", "start", "end", "description", "location")
    success_url = reverse_lazy("friendscal:index")
    template_name = "friendscal/appointment_update.html"

    def get_form(self, form_class=None):
        form = super(AppointmentUpdateView, self).get_form(form_class)
        form.fields["start"].widget.attrs.update({"class": "datepicker"})
        # form.fields['start'].widget.attrs.update(input_format='%d.%m.%Y')
        form.fields["end"].widget.attrs.update({"class": "datepicker"})
        return form

    def form_valid(self, form):
        if form.cleaned_data['end'] < form.cleaned_data['start']:
            raise forms.ValidationError("End date must be later than start date")
        return super(AppointmentUpdateView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class AppointmentDeleteView(generic.DeleteView):
    model = Appointment
    success_url = reverse_lazy("friendscal:index")

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

    data = Appointment.objects.filter(user__in=users, end__range=(start, end)).values() | Appointment.objects.filter(user=request.user, end__range=(start, end)).values()

    data = [item for item in data]
    for counter, element in enumerate(data):
        data[counter]['id'] = str(element['uuid'])
        del data[counter]['uuid']
    #return JsonResponse(json.dumps(data, ensure_ascii=False), safe=False)
    return JsonResponse(data, safe=False)

