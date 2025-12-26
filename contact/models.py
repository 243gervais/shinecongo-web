from django.db import models


class ContactMessage(models.Model):
    """Modèle pour les messages de contact"""
    
    name = models.CharField("Nom", max_length=200)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    subject = models.CharField("Sujet", max_length=300)
    message = models.TextField("Message")
    
    # Métadonnées
    created_at = models.DateTimeField("Date d'envoi", auto_now_add=True)
    read = models.BooleanField("Lu", default=False)
    replied = models.BooleanField("Répondu", default=False)
    notes = models.TextField("Notes internes", blank=True)
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
