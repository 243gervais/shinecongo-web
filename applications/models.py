from django.db import models
from django.core.validators import FileExtensionValidator


def cv_upload_path(instance, filename):
    """Chemin de téléchargement pour les CVs"""
    return f'cvs/{instance.email}/{filename}'


class JobApplication(models.Model):
    """Modèle pour les candidatures d'emploi"""
    
    full_name = models.CharField("Nom complet", max_length=200)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=20)
    city = models.CharField("Ville", max_length=100)
    position_applied = models.CharField("Poste souhaité", max_length=200)
    years_experience = models.IntegerField("Années d'expérience", default=0)
    availability_date = models.DateField("Date de disponibilité", null=True, blank=True)
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
        return f"{self.full_name} - {self.position_applied}"
