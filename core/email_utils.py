from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_application_notification(application):
    """Envoie une notification email lors d'une nouvelle candidature"""
    
    subject = f'Nouvelle candidature: {application.full_name}'
    
    # Préparer le contenu
    cv_url = application.cv_file.url if application.cv_file else 'Aucun CV'
    
    # Format date safely
    date_of_birth_str = application.date_of_birth.strftime('%d/%m/%Y') if application.date_of_birth else 'Non spécifiée'
    physical_address_str = application.physical_address or 'Non spécifiée'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #003B5C;">Nouvelle Candidature Reçue</h2>
        
        <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2A9D8F; margin-top: 0;">Informations du Candidat</h3>
            <p><strong>Nom:</strong> {application.full_name}</p>
            <p><strong>Date de naissance:</strong> {date_of_birth_str}</p>
            <p><strong>Téléphone:</strong> {application.phone}</p>
            <p><strong>Ville:</strong> {application.city}</p>
            <p><strong>Adresse physique:</strong> {physical_address_str}</p>
        </div>
        
        <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2A9D8F; margin-top: 0;">Message</h3>
            <p>{application.message or 'Aucun message'}</p>
        </div>
        
        <div style="margin: 20px 0;">
            <p><strong>CV:</strong> <a href="{cv_url}" style="color: #E76F51;">Télécharger le CV</a></p>
        </div>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="color: #666; font-size: 12px;">
            Cette candidature a été reçue via le site web Shine Congo le {application.applied_at.strftime('%d/%m/%Y à %H:%M')}.
        </p>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False


def send_contact_notification(contact_message):
    """Envoie une notification email lors d'un nouveau message de contact"""
    
    subject = f'Nouveau message: {contact_message.subject}'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #003B5C;">Nouveau Message de Contact</h2>
        
        <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2A9D8F; margin-top: 0;">Informations de l'Expéditeur</h3>
            <p><strong>Nom:</strong> {contact_message.name}</p>
            <p><strong>Email:</strong> {contact_message.email}</p>
            <p><strong>Téléphone:</strong> {contact_message.phone or 'Non fourni'}</p>
        </div>
        
        <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2A9D8F; margin-top: 0;">Sujet</h3>
            <p>{contact_message.subject}</p>
        </div>
        
        <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2A9D8F; margin-top: 0;">Message</h3>
            <p>{contact_message.message}</p>
        </div>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="color: #666; font-size: 12px;">
            Ce message a été reçu via le formulaire de contact le {contact_message.created_at.strftime('%d/%m/%Y à %H:%M')}.
        </p>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False
