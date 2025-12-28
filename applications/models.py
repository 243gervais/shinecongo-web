from django.db import models
from django.core.validators import FileExtensionValidator


def cv_upload_path(instance, filename):
    """Chemin de téléchargement pour les CVs"""
    # Use full_name for folder structure
    # Make the name safe for filesystem
    if instance.nom and instance.prenom:
        safe_name = f"{instance.nom}_{instance.prenom}".replace(' ', '_').replace('/', '_').replace('\\', '_')
    elif instance.full_name:
        safe_name = instance.full_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    else:
        safe_name = 'candidate'
    # Remove any other problematic characters
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('_', '-'))
    if not safe_name:
        safe_name = 'candidate'
    return f'cvs/{safe_name}/{filename}'


class JobApplication(models.Model):
    """Modèle pour les candidatures d'emploi"""
    
    APPLICATION_TYPE_CHOICES = [
        ('MANUAL', 'Remplir manuellement'),
        ('CV_UPLOAD', 'Télécharger mon CV'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    HOW_HEARD_CHOICES = [
        ('AFFICHE', 'Affiche'),
        ('MOTEUR_RECHERCHE', 'Moteur de recherche'),
        ('PERSONNE', 'A travers une personne'),
    ]
    
    # Type d'application
    application_type = models.CharField(
        "Type de candidature",
        max_length=20,
        choices=APPLICATION_TYPE_CHOICES,
        default='MANUAL'
    )
    
    # Informations personnelles - Section 1
    nom = models.CharField("Nom", max_length=100, blank=True, null=True)
    post_nom = models.CharField("Post-nom", max_length=100, blank=True, null=True)
    prenom = models.CharField("Prénom", max_length=100, blank=True, null=True)
    full_name = models.CharField("Nom complet", max_length=200, blank=True, null=True)  # Keep for backward compatibility
    date_of_birth = models.DateField("Date de naissance", null=True, blank=True)
    lieu_de_naissance = models.CharField("Lieu de naissance", max_length=200, blank=True, null=True)
    sexe = models.CharField("Sexe", max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    nationalite = models.CharField("Nationalité", max_length=100, blank=True, null=True)
    physical_address = models.TextField("Adresse physique", max_length=500, blank=True, null=True)
    phone = models.CharField("Téléphone", max_length=20)
    city = models.CharField("Ville", max_length=100, blank=True, null=True)
    
    # Comment avez-vous connu la company - Section 2
    how_heard_about = models.CharField(
        "Comment avez-vous connu Shine Congo?",
        max_length=20,
        choices=HOW_HEARD_CHOICES,
        blank=True
    )
    how_heard_details = models.CharField(
        "Détails",
        max_length=300,
        blank=True,
        null=True,
        help_text="Où avez-vous vu l'affiche / Quel moteur de recherche / Nom de la personne"
    )
    
    # Etude faites - Section 3
    education = models.TextField(
        "Études faites",
        blank=True,
        null=True,
        help_text="Exemple: Diplôme d'État en Sciences Commerciales et Gestion (2018-2021) - Institut X, Kinshasa"
    )
    
    # Competences et profil - Section 4
    skills = models.TextField(
        "Compétences et profil",
        blank=True,
        null=True,
        help_text="Exemple: Maîtrise de Microsoft Office, Bonne communication, Expérience en service client, Capacité à travailler en équipe"
    )
    
    # Langue parler - Section 5
    languages = models.CharField(
        "Langues parlées",
        max_length=200,
        blank=True,
        null=True,
        help_text="Exemple: Français (courant), Lingala (maternelle), Anglais (notions)"
    )
    
    # CV et message (optionnels pour remplissage manuel)
    cv_file = models.FileField(
        "CV (PDF/DOC/DOCX)",
        upload_to=cv_upload_path,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        blank=True,
        null=True,
        help_text="Formats acceptés: PDF, DOC, DOCX. Taille max: 5MB"
    )
    message = models.TextField("Message / Lettre de motivation", blank=True)
    
    # Métadonnées
    applied_at = models.DateTimeField("Date de candidature", auto_now_add=True)
    reviewed = models.BooleanField("Examiné", default=False)
    notes = models.TextField("Notes internes", blank=True)
    
    class Meta:
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        ordering = ['-applied_at']
    
    def __str__(self):
        if self.nom and self.prenom:
            name = f"{self.nom} {self.prenom}"
        elif self.full_name:
            name = self.full_name
        else:
            name = "Candidat"
        dob_str = self.date_of_birth.strftime('%d/%m/%Y') if self.date_of_birth else 'N/A'
        return f"{name} - {dob_str}"
