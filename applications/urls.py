from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('postuler/', views.JobApplicationView.as_view(), name='apply'),
    path('confirmation/', views.ApplicationSuccessView.as_view(), name='success'),
    path('cv/<int:pk>/', views.view_cv_pdf, name='view_cv_pdf'),
]
