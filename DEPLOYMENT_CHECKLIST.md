# Shine Congo - Checklist de Déploiement 🚀

## ✅ Configuration Immédiate Requise

### 1. Variables d'Environnement (.env en production)

- [ ] **SECRET_KEY**: Générer une nouvelle clé sécurisée
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```

- [ ] **DEBUG**: Définir à `False`

- [ ] **ALLOWED_HOSTS**: Ajouter votre domaine
  ```
  ALLOWED_HOSTS=shinecongo.com,www.shinecongo.com
  ```

- [ ] **CSRF_TRUSTED_ORIGINS**: Ajouter vos URLs avec HTTPS
  ```
  CSRF_TRUSTED_ORIGINS=https://shinecongo.com,https://www.shinecongo.com
  ```

### 2. Base de Données PostgreSQL

- [ ] Créer la base de données
- [ ] Créer l'utilisateur
- [ ] Configurer DATABASE_URL
  ```
  DATABASE_URL=postgres://shineuser:password@localhost:5432/shinecongo
  ```

### 3. AWS Lightsail Object Storage

- [ ] Créer un bucket (ex: `shinecongo-uploads`)
- [ ] Générer les clés d'accès
- [ ] Configurer dans .env:
  - `AWS_ACCESS_KEY_ID=`
  - `AWS_SECRET_ACCESS_KEY=`
  - `AWS_STORAGE_BUCKET_NAME=`
  - `AWS_S3_ENDPOINT_URL=`
  - `AWS_S3_REGION_NAME=`

### 4. Email SMTP (SendGrid/SES)

- [ ] Créer un compte SendGrid ou configurer AWS SES
- [ ] Générer une API key
- [ ] Configurer dans .env:
  - `EMAIL_HOST=smtp.sendgrid.net`
  - `EMAIL_HOST_USER=apikey`
  - `EMAIL_HOST_PASSWORD=votre-api-key`
  - `DEFAULT_FROM_EMAIL=noreply@shinecongo.com`
  - `ADMIN_EMAIL=admin@shinecongo.com`

## 📝 Personnalisation du Contenu

### 5. Informations de Contact

Dans `templates/base.html` (footer) et `templates/contact/contact.html`:
- [ ] Remplacer `+243 XXX XXX XXX` par le vrai numéro
- [ ] Remplacer `contact@shinecongo.com` par le vrai email
- [ ] Ajouter l'adresse physique exacte

### 6. Tarifs des Services

Dans `templates/core/home.html` et `templates/core/services.html`:
- [ ] Remplacer tous les `XXX FC` par les vrais prix
- [ ] Mettre à jour les descriptions de services si nécessaire

### 7. Google Maps

Dans `templates/contact/contact.html`:
- [ ] Intégrer le widget Google Maps avec votre adresse
- [ ] Obtenir une API key Google Maps

### 8. Réseaux Sociaux

Dans `templates/base.html` (footer):
- [ ] Ajouter les liens Facebook
- [ ] Ajouter les liens Instagram
- [ ] Ajouter les liens LinkedIn
- [ ] Ajouter le numéro WhatsApp Business

## 👤 Configuration Admin

### 9. Créer les Comptes Admin

```bash
python manage.py createsuperuser
```

### 10. Ajouter les Postes Disponibles

Via l'admin Django (https://votre-domaine.com/admin):
- [ ] Créer au moins 2-3 offres d'emploi actives
- [ ] Exemples suggérés:
  - Laveur de Voitures
  - Superviseur d'Équipe
  - Réceptionniste/Caissier
  - Technicien Detailing

## 🔒 Sécurité et SSL

### 11. Certificat SSL

```bash
sudo certbot --nginx -d shinecongo.com -d www.shinecongo.com
```

### 12. Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 🧪 Tests Avant Lancement

### 13. Tester les Fonctionnalités

- [ ] Tester le formulaire de candidature avec upload de CV
- [ ] Vérifier que le CV arrive bien sur S3
- [ ] Tester le formulaire de contact
- [ ] Vérifier la réception des emails (candidature + contact)
- [ ] Tester l'admin Django (visualiser candidatures, télécharger CVs)
- [ ] Vérifier le responsive sur mobile
- [ ] Tester tous les liens de navigation

### 14. SEO & Analytics (Optionnel)

- [ ] Ajouter Google Analytics
- [ ] Créer un sitemap.xml
- [ ] Soumettre à Google Search Console
- [ ] Optimiser les meta descriptions si nécessaire

## 📊 Monitoring (Post-Lancement)

### 15. Surveillance

- [ ] Configurer les alertes par email pour les erreurs
- [ ] Vérifier les logs régulièrement
- [ ] Monitor l'espace disque
- [ ] Monitor l'utilisation du bucket S3

### 16. Backup

- [ ] Mettre en place un backup automatique de la base de données
  ```bash
  # Créer un cron job pour backup quotidien
  0 2 * * * cd /var/www/shinecongo && ./backup.sh
  ```

## 🎨 Optionnel (Améliorations Futures)

- [ ] Intégrer un système de paiement mobile (Airtel Money, M-Pesa)
- [ ] Ajouter un système de réservation en ligne
- [ ] Créer une app mobile (React Native/Flutter)
- [ ] Ajouter un dashboard client pour suivre l'historique
- [ ] Intégrer un chatbot WhatsApp

## 📧 Emails de Test

Avant le lancement, envoyez des emails de test à:
- [ ] Vous-même
- [ ] Collègue/ami
- [ ] Vérifier qu'ils n'arrivent pas en spam

## 🎯 Go Live!

Une fois tout coché ci-dessus:
- [ ] Annoncer le lancement sur les réseaux sociaux
- [ ] Envoyer un email à votre base de clients existants
- [ ] Imprimer des flyers/cartes avec l'URL du site
- [ ] Former l'équipe à utiliser l'admin Django

---

**Notes importantes:**
- Gardez une copie de `.env` dans un endroit sécurisé (pas sur Git!)
- Documentez tous les mots de passe dans un gestionnaire sécurisé
- Testez d'abord sur un domaine de staging si possible

Bonne chance! 🎉
