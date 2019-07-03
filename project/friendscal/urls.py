from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'friendscal'
urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='friendscal/index.html')), name='index'),
]