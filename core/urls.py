from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('media/', include([
        path('profile/<str:name>', views.ProfileMediaView.as_view(), name="profile_media"),
    ])),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register_view, name='register'),

    path('accounts/', include([
        path('profile/', views.ProfileView.as_view(), name='profile'),
        path('mytests/', views.MyTestsView.as_view(), name='mytests'),
    ])),
]
