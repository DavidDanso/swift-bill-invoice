from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('dashboard', views.dashboardPage, name='dashboard'),
    path('invoice', views.create_invoice, name='invoice'),
    path('clients', views.create_client, name='clients'),

    path('client/<str:pk>', views.edit_client, name='client-details'),
    path('invoice/<str:pk>', views.edit_invoice, name='invoice-details'),

    path('preview-invoice/<str:pk>', views.preview_invoice, name='preview-invoice'),
]