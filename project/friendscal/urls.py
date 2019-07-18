from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'friendscal'
urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='friendscal/index.html')), name='index'),
    path('create/', views.AppointmentCreateView.as_view(), name='create'),
    path('<uuid:pk>/update/', views.AppointmentUpdateView.as_view(), name='change'),
    path('<uuid:pk>/detail/', views.AppointmentDetailView.as_view(), name='detail'),
    path('<uuid:pk>/delete/', views.AppointmentDeleteView.as_view(), name='delete'),
]