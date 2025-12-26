from django.views.generic import ListView, DetailView
from .models import JobRole


class CareersListView(ListView):
    """Liste des postes disponibles"""
    model = JobRole
    template_name = 'careers/careers_list.html'
    context_object_name = 'roles'
    
    def get_queryset(self):
        return JobRole.objects.filter(is_active=True)


class JobDetailView(DetailView):
    """Détail d'un poste"""
    model = JobRole
    template_name = 'careers/job_detail.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        return JobRole.objects.filter(is_active=True)
