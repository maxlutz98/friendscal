from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'friendscal'
urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='friendscal/index.html')), name='index'),
    path('appointment/create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointment/<uuid:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment-change'),
    path('appointment/<uuid:pk>/detail/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointment/<uuid:uuid>/json/', views.AppointmentJson, name='appointment-json'),
    path('appointment/<uuid:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('appointment/list/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointment/events/', views.events, name='appointment-events'),
    path('description/', TemplateView.as_view(template_name='friendscal/description.html'), name='description'),
    path('impressum/', TemplateView.as_view(template_name='friendscal/impressum.html'), name='impressum'),
    path('privacy/', TemplateView.as_view(template_name='friendscal/privacy.html'), name='privacy'),
]