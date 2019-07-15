from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('detail/', views.UserDetailView.as_view(), name='detail'),
    path('change/', views.UserUpdateView.as_view(), name='change'),
    path('password_change/', views.change_password, name='password_change'),
    path('delete/', views.UserDeleteView.as_view(), name='delete'),
    path('deleted/', TemplateView.as_view(template_name='users/user_deleted.html'), name='deleted'),
]