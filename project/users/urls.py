from django.urls import path, re_path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    re_path(r'^detail/$', views.MyUserDetailView.as_view(), name='userdetail'),
    re_path(r'^update/$', views.MyUserUpdateView.as_view(), name='userchange'),
    re_path(r'^update_password/$', views.change_password, name='change_password'),
]