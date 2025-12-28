from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import JobApplication
from .forms import ManualApplicationForm, CVUploadApplicationForm
from .pdf_utils import generate_cv_pdf
from core.email_utils import send_application_notification


class JobApplicationView(TemplateView):
    """Vue pour soumettre une candidature avec deux options"""
    template_name = 'applications/apply.html'
    
    def get(self, request, *args, **kwargs):
        manual_form = ManualApplicationForm()
        cv_form = CVUploadApplicationForm()
        return render(request, self.template_name, {
            'manual_form': manual_form,
            'cv_form': cv_form,
        })
    
    def post(self, request, *args, **kwargs):
        application_type = request.POST.get('application_type')
        
        if application_type == 'MANUAL':
            form = ManualApplicationForm(request.POST)
        elif application_type == 'CV_UPLOAD':
            form = CVUploadApplicationForm(request.POST, request.FILES)
        else:
            messages.error(request, 'Veuillez sélectionner un type de candidature.')
            manual_form = ManualApplicationForm()
            cv_form = CVUploadApplicationForm()
            return render(request, self.template_name, {
                'manual_form': manual_form,
                'cv_form': cv_form,
            })
        
        if form.is_valid():
            application = form.save()
            
            # Envoyer notification email (ne pas bloquer si l'email échoue)
            try:
                send_application_notification(application)
            except Exception as e:
                # Log l'erreur mais ne bloque pas la soumission
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Erreur lors de l'envoi de l'email de notification: {e}")
            
            messages.success(
                request,
                'Votre candidature a été envoyée avec succès! Nous vous contacterons bientôt.'
            )
            return redirect('applications:success')
        else:
            # Show specific field errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form.fields[field].label if field in form.fields else field
                    error_messages.append(f"{field_label}: {error}")
            
            if error_messages:
                messages.error(
                    request,
                    'Veuillez corriger les erreurs suivantes: ' + ' | '.join(error_messages)
                )
            else:
                messages.error(
                    request,
                    'Une erreur s\'est produite. Veuillez vérifier vos informations.'
                )
            
            # Return forms with errors
            if application_type == 'MANUAL':
                manual_form = form
                cv_form = CVUploadApplicationForm()
            else:
                manual_form = ManualApplicationForm()
                cv_form = form
            
            return render(request, self.template_name, {
                'manual_form': manual_form,
                'cv_form': cv_form,
            })


class ApplicationSuccessView(TemplateView):
    """Page de confirmation après candidature"""
    template_name = 'applications/success.html'


@staff_member_required
def view_cv_pdf(request, pk):
    """View PDF CV for manual applications"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    # Only generate PDF for manual applications
    if application.application_type == 'MANUAL':
        pdf = generate_cv_pdf(application)
        
        # Create filename
        if application.nom and application.prenom:
            filename = f"CV_{application.prenom}_{application.nom}.pdf"
        elif application.full_name:
            filename = f"CV_{application.full_name.replace(' ', '_')}.pdf"
        else:
            filename = f"CV_{application.id}.pdf"
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    else:
        # For CV upload applications, redirect to the uploaded file
        if application.cv_file:
            return redirect(application.cv_file.url)
        else:
            messages.error(request, 'Aucun CV disponible pour cette candidature.')
            return redirect('admin:applications_jobapplication_changelist')
