
from django.urls import path
from . import views

urlpatterns = [
    path("theme", views.theme, name="theme"),
    path('user/auth', views.auth, name='auth'),
    path('user/logout', views.logout_user, name='logout'),
    path('user/dashboard', views.user_dashboard, name='dash'),
    path('user/update-profile', views.profile_update, name='user.profile.update'),
    path('user/update-address', views.address_update, name='user.address.update'),
    path('user/edit-profile', views.profile_edit, name='user.profile.edit'),
    path('user/edit-address', views.address_edit, name='user.address.edit'),
]
