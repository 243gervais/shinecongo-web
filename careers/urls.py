from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.RoleExplanationView.as_view(), name='list'),
    path('role/', views.RoleExplanationView.as_view(), name='role_explanation'),
    path('<slug:slug>/', views.JobDetailView.as_view(), name='detail'),
]
