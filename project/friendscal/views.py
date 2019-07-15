from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .models import Appointment

# Create your views here.
def index(request):
    return HttpResponse('HELLO FROM FRIENDSCAL')

class AppointmentCreateView(generic.CreateView):
    model = Appointment
    fields = ('title', 'start', 'end', 'description', 'location',)
    success_url = reverse_lazy('friendscal:index')
    template_name = 'friendscal/appointment_create.html'

    def get_form(self):
        form = super(AppointmentCreateView, self).get_form()
        form.fields['start'].widget.attrs.update({'class': 'datepicker'})
#        form.fields['start'].widget.attrs.update(input_format='%d.%m.%Y')
        form.fields['end'].widget.attrs.update({'class': 'datepicker'})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AppointmentCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class AppointmentDetailView(generic.DetailView):
    model = Appointment
    template_name = 'friendscal/appointment_detail.html'


@method_decorator(login_required, name='dispatch')
class AppointmentUpdateView(generic.UpdateView):
    model = Appointment
    success_url = reverse_lazy('friendscal:detail')
    template_name = 'friendscal/appointment_update.html'

@method_decorator(login_required, name='dispatch')
class AppointmentDeleteView(generic.DeleteView):
    model = Appointment
    template_name = 'friendscal/appointment_delete.html'
    success_url = reverse_lazy('friendscal:index')