from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    re_path(r'^detail/$', views.UserDetailView.as_view(), name='detail'),
    re_path(r'^edit/$', views.UserUpdateView.as_view(), name='change'),
    re_path(r'^update_password/$', views.change_password, name='change_password'),
    path('delete/', views.UserDeleteView.as_view(), name='delete'),
    path('deleted/', TemplateView.as_view(template_name='users/deleted.html'), name='deleted'),
]