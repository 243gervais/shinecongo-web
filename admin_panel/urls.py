from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    
    # Applications
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/download-cv/', views.download_cv, name='download_cv'),
    
    # Jobs
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    
    # Messages
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    
    # Logout
    path('logout/', views.admin_logout, name='logout'),
]

