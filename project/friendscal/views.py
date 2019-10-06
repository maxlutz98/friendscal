from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .models import Appointment
from users.models import User

import datetime


# Create your views here.

@method_decorator(login_required, name="dispatch")
class AppointmentCreateView(generic.CreateView):
    """
    View zur Erstellung von Appointments.
    """
    model = Appointment
    fields = ("title", "start", "end", "description", "location")
    success_url = reverse_lazy("friendscal:index")
    template_name = "friendscal/appointment_create.html"

    def get_form(self, form_class=None):
        """
        Anpassung des Formulars.
        Deutsches Datums-/Zeitformat für DateTime-Felder.
        Date-/Timepciker für DateTime-Felder.
        """
        form = super(AppointmentCreateView, self).get_form(form_class)
        form.fields['start'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields['end'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields["start"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M',
                                                                date_attrs={"class": "datepicker"},
                                                                time_attrs={"class": "timepicker"})
        form.fields["end"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M',
                                                              date_attrs={"class": "datepicker"},
                                                              time_attrs={"class": "timepicker"})
        return form

    def form_valid(self, form):
        """
        Validierung des Formulars angepasst.
        Fehlermeldung bei Enddatum vor Startdatum
        """
        form.instance.user = self.request.user
        if form.cleaned_data['end'] < form.cleaned_data['start']:
            raise forms.ValidationError("End date must be later than start date")
        return super(AppointmentCreateView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class AppointmentDetailView(generic.DetailView):
    """
    View zur Detail Ansicht eines Appointments.
    """
    model = Appointment
    template_name = "friendscal/appointment_detail.html"


@method_decorator(login_required, name="dispatch")
class AppointmentUpdateView(UserPassesTestMixin, generic.UpdateView):
    """
    View zum Ändern eines Appointments.
    Zusätzlich ein Berechtigungstest für den User.
    """
    model = Appointment
    fields = ("title", "start", "end", "description", "location")
    success_url = reverse_lazy("friendscal:index")
    template_name = "friendscal/appointment_update.html"

    def test_func(self):
        """
        Test, der bestanden werden muss, um die View einzusehen.
        """
        return self.request.user == Appointment.objects.get(pk=self.kwargs['pk']).user

    def get_form(self, form_class=None):
        """
        Anpassung des Formulars.
        Deutsches Datums-/Zeitformat für DateTime-Felder.
        Date-/Timepciker für DateTime-Felder.
        """
        form = super(AppointmentUpdateView, self).get_form(form_class)
        form.fields['start'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields['end'] = forms.SplitDateTimeField(input_date_formats=settings.DATE_INPUT_FORMATS)
        form.fields["start"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M',
                                                                date_attrs={"class": "datepicker"},
                                                                time_attrs={"class": "timepicker"})
        form.fields["end"].widget = forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M',
                                                              date_attrs={"class": "datepicker"},
                                                              time_attrs={"class": "timepicker"})
        return form

    def form_valid(self, form):
        """
        Validierung des Formulars angepasst.
        Fehlermeldung bei Enddatum vor Startdatum
        """
        if form.cleaned_data['end'] < form.cleaned_data['start']:
            raise forms.ValidationError("End date must be later than start date")
        return super(AppointmentUpdateView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class AppointmentDeleteView(UserPassesTestMixin, generic.DeleteView):
    """
    View zum Löschen eines Appointments.
    Zusätzlich ein Berechtigungstest für den User.
    """
    model = Appointment
    success_url = reverse_lazy("friendscal:index")

    def test_func(self):
        """
        Test, der bestanden werden muss, um die View einzusehen.
        """
        return self.request.user == Appointment.objects.get(pk=self.kwargs['pk']).user


@method_decorator(login_required, name="dispatch")
class AppointmentListView(generic.ListView):
    """
    View zu Erzeugung einer Listenansicht der Nutzer zugehörigen Appointments.
    """
    model = Appointment

    def get_queryset(self):
        """
        Anpassung der gesammelten Appointments:
        - nur Appointments des aufrufenden Nutzers
        - nur Appointments, welche noch nicht vorbei sind
        """
        queryset = self.request.user.appointment_set.all().filter(end__gte=datetime.datetime.today()).order_by('start')
        return queryset

    def get_context_data(self, *args, **kwargs):
        """
        Sammeln zusätzlicher Informationen:
        - alle vergangen Appointments des Nutzers in den letzten 2 Jahren
        """
        context = super(AppointmentListView, self).get_context_data(*args, **kwargs)
        context["past_list"] = self.request.user.appointment_set.all().filter(
            end__range=(datetime.datetime.today() - datetime.timedelta(days=730), datetime.datetime.today())).order_by(
            '-end')
        return context


@login_required
def events(request):
    """
    View zur Rückgabe aller Appointments eines Nutzers innerhalb eines gewissen Zeitraums als JSON.
    """
    # GET Parameter Informationen der Anfrage auslesen.
    start = request.GET.get('start')
    end = request.GET.get('end')
    user = request.GET.get('user')
    user = User.objects.get(username=user)
    # Appointment mithilfe der Parameter filtern (Zeitraum und Nutzer)
    if user in request.user.shared_by.all() or request.user == user:
        data = Appointment.objects.filter(Q(user=user), Q(end__range=(start, end)) | Q(start__range=(start, end)) | (
                    Q(start__lte=start) & Q(end__gte=end))).values()
    else:
        data = []

    # Konvertierung des Querysets zu einer Liste aus Dictionaries und Hinzufügen der UUID als ID
    # Daten als JSON zurückgeben
    data = [item for item in data]
    print(data)
    for counter, element in enumerate(data):
        data[counter]['id'] = str(element['uuid'])
        del data[counter]['uuid']
    # Rückgabe der Liste mit dem Parameter "safe=False", da normalerweise mit reinen Dictionaries gearbeitet wird.
    return JsonResponse(data, safe=False)


@login_required
def AppointmentJson(request, uuid):
    """
    View zur Rückgabe eines Appointments anhand der UUID als JSON.
    """
    # Appointment erhalten
    appointment = Appointment.objects.get(pk=uuid)

    # Appointment Informationen in ein Dictionary packen
    data = {
        'uuid': str(appointment.uuid),
        'title': appointment.title,
        'start': '{dt:%d.%m.%Y %H:%M}'.format(dt=appointment.start),
        'end': '{dt:%d.%m.%Y %H:%M}'.format(dt=appointment.end),
        'description': appointment.description,
        'location': appointment.location,
        'user': appointment.user.get_full_name()
    }

    # Hinzufügen eines 'can_edit' Attributs, falls der anfragende Nutzer Inhaber des Appointments ist
    if request.user == appointment.user:
        data['can_edit'] = True

    return JsonResponse(data)


@login_required
def SessionAdd(request):
    """
    Hinzufügen des übermittelten Nutzername zur Speicherung in der Session Information.
    """
    if request.method == 'POST':
        # POST Parameter auslesen
        name = request.POST.get("checked", "")

        # Erhalten des entsprechenden Nutzer Objektes
        user = User.objects.get(username=name)
        # nur bearbeiten, wenn Nutzer der Anfragesteller selbst oder ein Nutzer, welcher dem Anfragesteller eine Freigabe erteilt hat, ist.
        if user in request.user.shared_by.all() or request.user == user:
            # Überprüfen, ob es bereits den Key "checked" im Session Dictionary gibt
            if not "checked" in request.session.keys():
                # nicht existent:
                # Erstellen einer leeren Liste, Nutzername hinzufügen und dem Session Dic zuweisen
                # (Direkt dem Session Dic hinzufügen ist nicht möglich, da es nicht gespeichert wird)
                thislist = []
                thislist.append(name)
                request.session["checked"] = thislist
            else:
                # existent:
                # Überprüfung, ob Nutzername bereits vorhanden ist
                # -> Auslesen der Liste, Nutzername hinzufügen und wieder dem Session Dic zuweisen
                # (Direkt dem Session Dic hinzufügen ist nicht möglich, da es nicht gespeichert wird)
                if not name in request.session["checked"]:
                    thislist = request.session["checked"]
                    thislist.append(name)
                    request.session["checked"] = thislist
    # leere Rückgabe, da eine Rückgabe benötigt wird
    return JsonResponse({})


@login_required
def SessionRemove(request):
    """
    Entfernen des übermittelten Nutzernamen aus der Session Information.
    """
    if request.method == 'POST':
        # POST Parameter auslesen
        name = request.POST.get("checked", "")

        # Überprüfen, ob es bereits den Key "checked" im Session Dictionary gibt
        if "checked" in request.session.keys():
            # Überprüfung, ob Nutzername vorhanden ist
            # -> Entfernen des Nutzernamens
            # (Direkt aus dem Session Dic entfernen ist nicht möglich, da es nicht gespeichert wird)
            if name in request.session["checked"]:
                thislist = request.session["checked"]
                thislist.remove(name)
                request.session["checked"] = thislist
    # leere Rückgabe, da eine Rückgabe benötigt wird
    return JsonResponse({})
