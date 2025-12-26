from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('a-propos/', views.AboutView.as_view(), name='about'),
    path('confidentialite/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('conditions/', views.TermsView.as_view(), name='terms'),
]
