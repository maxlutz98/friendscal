from django.urls import path, re_path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    re_path(r'^detail/(?P<pk>\d+)/$', views.MyUserDetailView.as_view(), name='myuserdetail'),
    re_path(r'^update/(?P<pk>\d+)/$', views.MyUserUpdateView.as_view(), name='myuserupdate'),
    re_path(r'^update_password/(?P<pk>\d+)/$', views.MyUserPWUpdateView.as_view(), name='myuserpwupdate'),
]