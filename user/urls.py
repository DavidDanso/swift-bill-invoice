from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profilePage, name='profile'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('signup', views.signupPage, name='signup'),

    # 
    path('welcome_email', views.welcomeEmail, name='welcome_email'),
]