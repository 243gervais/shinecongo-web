from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import redirect
from .models import JobRole


class RoleExplanationView(TemplateView):
    """Page d'explication du rôle avant candidature"""
    template_name = 'careers/role_explanation.html'


class CareersListView(ListView):
    """Liste des postes disponibles"""
    model = JobRole
    template_name = 'careers/careers_list.html'
    context_object_name = 'roles'
    
    def get_queryset(self):
        return JobRole.objects.filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        # Redirect to role explanation page since we only have one position
        return redirect('careers:role_explanation')


class JobDetailView(DetailView):
    """Détail d'un poste"""
    model = JobRole
    template_name = 'careers/job_detail.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        return JobRole.objects.filter(is_active=True)
