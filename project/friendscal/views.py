from django.http import HttpResponse
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

    def get_form(self):
        form = super(AppointmentCreateView, self).get_form()
        form.fields["start"].widget.attrs.update({"class": "datepicker"})
        #        form.fields['start'].widget.attrs.update(input_format='%d.%m.%Y')
        form.fields["end"].widget.attrs.update({"class": "datepicker"})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
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

