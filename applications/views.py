from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import JobApplication
from .forms import JobApplicationForm
from core.email_utils import send_application_notification


class JobApplicationView(CreateView):
    """Vue pour soumettre une candidature"""
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'applications/apply.html'
    success_url = reverse_lazy('applications:success')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Envoyer notification email
        send_application_notification(self.object)
        
        messages.success(
            self.request,
            'Votre candidature a été envoyée avec succès! Nous vous contacterons bientôt.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Une erreur s\'est produite. Veuillez vérifier vos informations.'
        )
        return super().form_invalid(form)


class ApplicationSuccessView(TemplateView):
    """Page de confirmation après candidature"""
    template_name = 'applications/success.html'
