from django.db import models
from django.core.validators import FileExtensionValidator


def cv_upload_path(instance, filename):
    """Chemin de téléchargement pour les CVs"""
    # Use full_name instead of email for folder structure
    # Make the name safe for filesystem
    safe_name = instance.full_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    # Remove any other problematic characters
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('_', '-'))
    if not safe_name:
        safe_name = 'candidate'
    return f'cvs/{safe_name}/{filename}'


class JobApplication(models.Model):
    """Modèle pour les candidatures d'emploi"""
    
    full_name = models.CharField("Nom complet", max_length=200)
    physical_address = models.TextField("Adresse physique", max_length=500)
    phone = models.CharField("Téléphone", max_length=20)
    city = models.CharField("Ville", max_length=100)
    date_of_birth = models.DateField("Date de naissance")
    message = models.TextField("Message / Lettre de motivation", blank=True)
    cv_file = models.FileField(
        "CV (PDF/DOC/DOCX)",
        upload_to=cv_upload_path,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        help_text="Formats acceptés: PDF, DOC, DOCX. Taille max: 5MB"
    )
    
    # Métadonnées
    applied_at = models.DateTimeField("Date de candidature", auto_now_add=True)
    reviewed = models.BooleanField("Examiné", default=False)
    notes = models.TextField("Notes internes", blank=True)
    
    class Meta:
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        ordering = ['-applied_at']
    
    def __str__(self):
        dob_str = self.date_of_birth.strftime('%d/%m/%Y') if self.date_of_birth else 'N/A'
        return f"{self.full_name} - {dob_str}"
