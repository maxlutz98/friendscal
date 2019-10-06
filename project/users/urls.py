from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'users'
urlpatterns = [
    path('detail/', views.UserDetailView.as_view(), name='user-detail'),
    path('change/', views.UserUpdateView.as_view(), name='user-change'),
    path('password_change/', views.change_password, name='user-password_change'),
    path('delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('deleted/', TemplateView.as_view(template_name='users/user_deleted.html'), name='user-deleted'),
    path('shares/', views.share_calendar, name='shares-detail'),
    # path('shares/change/', views.UserSharesUpdateView.as_view(), name='shares-change'),
    path('shares/remove/', views.unshare_calendar, name='shares-remove'),
    path('invitations/remove/', views.remove_invitation, name='invitation-remove'),
]
