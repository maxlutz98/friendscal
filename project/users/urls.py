from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='user-signup'),
    re_path(r'^detail/$', views.MyUserDetailView.as_view(), name='user-detail'),
    re_path(r'^edit/$', views.MyUserUpdateView.as_view(), name='user-change'),
    re_path(r'^update_password/$', views.change_password, name='change_password'),
    path('delete/', views.MyUserDeleteView.as_view(), name='user-delete'),
    path('deleted/', TemplateView.as_view(template_name='users/deleted.html'), name='user-deleted'),
]