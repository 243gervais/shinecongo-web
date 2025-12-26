from django.db import models


class JobRole(models.Model):
    """Modèle pour les postes disponibles chez Shine Congo"""
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Temps plein'),
        ('PART_TIME', 'Temps partiel'),
        ('CONTRACT', 'Contrat'),
    ]
    
    title = models.CharField("Titre du poste", max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField("Description")
    responsibilities = models.TextField("Responsabilités")
    requirements = models.TextField("Exigences")
    benefits = models.TextField("Avantages", blank=True)
    employment_type = models.CharField(
        "Type d'emploi",
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='FULL_TIME'
    )
    location = models.CharField("Lieu", max_length=200, default="Kinshasa, RDC")
    is_active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Poste"
        verbose_name_plural = "Postes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
