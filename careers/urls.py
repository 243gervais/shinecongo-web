from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.CareersListView.as_view(), name='list'),
    path('<slug:slug>/', views.JobDetailView.as_view(), name='detail'),
]
