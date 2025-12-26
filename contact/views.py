from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactForm
from core.email_utils import send_contact_notification


class ContactView(CreateView):
    """Vue pour envoyer un message de contact"""
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact:success')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Envoyer notification email
        send_contact_notification(self.object)
        
        messages.success(
            self.request,
            'Votre message a été envoyé avec succès! Nous vous répondrons bientôt.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Une erreur s\'est produite. Veuillez vérifier vos informations.'
        )
        return super().form_invalid(form)


class ContactSuccessView(TemplateView):
    """Page de confirmation après envoi de message"""
    template_name = 'contact/success.html'
