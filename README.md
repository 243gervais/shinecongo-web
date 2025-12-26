# Shine Congo - Website et Plateforme de Recrutement

Site web Django premium pour Shine Congo, service de lavage automobile à Kinshasa, RDC.

## 🚀 Fonctionnalités

### Site Public
- ✅ Page d'accueil moderne avec sections Hero, Services, Témoignages, FAQ
- ✅ Page Services détaillée (Lavage Basique, Premium Wash, Detailing Complet)
- ✅ Page À Propos (histoire, mission, valeurs)
- ✅ Page Carrières (liste des postes disponibles)
- ✅ Détail des postes avec descriptions complètes
- ✅ Formulaire de candidature avec upload de CV
- ✅ Formulaire de contact
- ✅ Pages Confidentialité et Conditions d'utilisation

### Fonctionnalités Techniques
- ✅ Upload de CV vers AWS Lightsail Object Storage (S3-compatible)
- ✅ Notifications email automatiques (candidatures + messages de contact)
- ✅ Interface d'administration Django complète
- ✅ Validation des fichiers CV (PDF, DOC, DOCX, max 5MB)
- ✅ Design responsive mobile-first avec Tailwind CSS
- ✅ Couleurs de marque Shine Congo
- ✅ PostgreSQL en production, SQLite en développement
- ✅ Configuration production-ready (Gunicorn, Nginx, systemd)
- ✅ Protection HTTPS et headers de sécurité
- ✅ Whitenoise pour fichiers statiques

## 📋 Prérequis

- Python 3.11+
- PostgreSQL 14+ (production)
- AWS Lightsail Object Storage ou S3-compatible bucket
- Compte SMTP (SendGrid, AWS SES, ou autre)

## 🛠️ Installation Locale (Développement)

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/shinecongo-web.git
cd ShineCongo-Web
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet (copier depuis `.env.example`):

```env
SECRET_KEY=votre-cle-secrete-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Database - Leave empty for SQLite
DATABASE_URL=

# Email (pour dev, laissez vide)
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@shinecongo.local
ADMIN_EMAIL=admin@shinecongo.local

# AWS S3 (pour dev, laissez vide pour utiliser stockage local)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_ENDPOINT_URL=
```

### 5. Effectuer les migrations

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 7. Créer des données d'exemple (optionnel)

```bash
python manage.py shell
```

```python
from careers.models import JobRole

JobRole.objects.create(
    title="Laveur de Voitures",
    slug="laveur-de-voitures",
    description="Rejoignez notre équipe de lavage professionnel.",
    responsibilities="- Effectuer le lavage extérieur des véhicules\n- Aspiration intérieure\n- Nettoyage des vitres",
    requirements="- Aucune expérience requise, formation fournie\n- Bon relationnel\n- Ponctualité",
    benefits="- Salaire compétitif\n- Formation continue\n- Environnement dynamique",
    employment_type="FULL_TIME",
    is_active=True
)
exit()
```

### 8. Lancer le serveur de développement

```bash
python manage.py runserver
```

Accédez à `http://localhost:8000` pour voir le site.  
Admin: `http://localhost:8000/admin`

## 🚢 Déploiement sur AWS Lightsail (Production)

### Prérequis Serveur
- Ubuntu 20.04/22.04 LTS
- Au moins 1GB RAM
- Nom de domaine configuré

### 1. Connexion et mise à jour du serveur

```bash
ssh ubuntu@votre-ip-lightsail
sudo apt update && sudo apt upgrade -y
```

### 2. Installation des dépendances

```bash
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

### 3. Configuration PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE shinecongo;
CREATE USER shineuser WITH PASSWORD 'VotreMotDePasseSecurise';
ALTER ROLE shineuser SET client_encoding TO 'utf8';
ALTER ROLE shineuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE shineuser SET timezone TO 'Africa/Kinshasa';
GRANT ALL PRIVILEGES ON DATABASE shinecongo TO shineuser;
\q
```

### 4. Créer la structure de répertoires

```bash
sudo mkdir -p /var/www/shinecongo
sudo chown $USER:$USER /var/www/shinecongo
cd /var/www/shinecongo
```

### 5. Cloner le projet

```bash
git clone https://github.com/votre-username/shinecongo-web.git .
```

### 6. Créer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Configurer les variables d'environnement

Créez le fichier `.env` en production:

```bash
nano .env
```

Remplissez avec vos vraies valeurs:

```env
SECRET_KEY=votre-cle-secrete-production-complexe
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
CSRF_TRUSTED_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com

# PostgreSQL
DATABASE_URL=postgres://shineuser:VotreMotDePasseSecurise@localhost:5432/shinecongo

# Email (SendGrid ou SES)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=votre-api-key-sendgrid
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@votre-domaine.com
ADMIN_EMAIL=admin@votre-domaine.com

# AWS Lightsail Object Storage
AWS_ACCESS_KEY_ID=votre-access-key
AWS_SECRET_ACCESS_KEY=votre-secret-key
AWS_STORAGE_BUCKET_NAME=shinecongo-uploads
AWS_S3_REGION_NAME=us-east-1
AWS_S3_ENDPOINT_URL=https://votre-region.amazonaws.com
AWS_S3_ADDRESSING_STYLE=path
```

### 8. Effectuer les migrations et collecter les fichiers statiques

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 9. Créer le dossier de logs

```bash
mkdir -p logs
sudo chown -R www-data:www-data /var/www/shinecongo
sudo chmod -R 755 /var/www/shinecongo
```

### 10. Configurer Gunicorn comme service systemd

```bash
sudo cp deployment/shinecongo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start shinecongo
sudo systemctl enable shinecongo
sudo systemctl status shinecongo
```

### 11. Configurer Nginx

```bash
sudo cp deployment/nginx-shinecongo.conf /etc/nginx/sites-available/shinecongo
sudo ln -s /etc/nginx/sites-available/shinecongo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 12. Configurer SSL avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

### 13. Vérification

Visitez `https://votre-domaine.com` pour voir le site en ligne!

## 📝 Configuration AWS Lightsail Object Storage

### 1. Créer un bucket

1. Connectez-vous à AWS Lightsail
2. Allez dans "Storage" > "Create bucket"
3. Nommez le bucket: `shinecongo-uploads`
4. Choisissez la région la plus proche (ex: us-east-1)

### 2. Créer les clés d'accès

1. Dans le bucket, allez dans "Permissions"
2. Créez une clé d'accès
3. Copiez l'Access Key ID et Secret Access Key

### 3. Configurer les permissions

Le bucket doit être **private** (les URL présignées seront utilisées pour l'accès aux CVs).

### 4. Endpoint URL

Format: `https://s3.us-east-1.amazonaws.com` (ou votre région)

## 🔧 Gestion et Maintenance

### Redémarrer l'application

```bash
sudo systemctl restart shinecongo
```

### Voir les logs

```bash
# Gunicorn logs
tail -f /var/www/shinecongo/logs/gunicorn-error.log
tail -f /var/www/shinecongo/logs/gunicorn-access.log

# Nginx logs
sudo tail -f /var/log/nginx/shinecongo-error.log
sudo tail -f /var/log/nginx/shinecongo-access.log

# Systemd logs
sudo journalctl -u shinecongo -f
```

### Mettre à jour le code

```bash
cd /var/www/shinecongo
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart shinecongo
```

### Backup de la base de données

```bash
sudo -u postgres pg_dump shinecongo > backup_$(date +%Y%m%d).sql
```

## 📧 Configuration Email

### Option 1: SendGrid (Recommandé)

1. Créez un compte sur sendgrid.com
2. Créez une API Key
3. Configurez dans `.env`:

```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=votre-api-key-sendgrid
```

### Option 2: AWS SES

1. Configurez AWS SES dans votre région
2. Vérifiez votre domaine
3. Créez des credentials SMTP
4. Configurez dans `.env`

## 👥 Administration

### Accéder à l'admin Django

`https://votre-domaine.com/admin`

### Gestion des candidatures

1. Connectez-vous à l'admin
2. Allez dans "Candidatures"
3. Vous pouvez:
   - Voir toutes les candidatures
   - Filtrer par poste, ville, date
   - Télécharger les CVs
   - Marquer comme examiné
   - Ajouter des notes internes

### Gestion des messages de contact

1. Dans l'admin, allez dans "Messages de contact"
2. Marquez comme lu/répondu
3. Ajoutez des notes

### Gestion des postes

1. Dans l'admin, allez dans "Postes"
2. Créez/modifiez des offres d'emploi
3. Activez/désactivez des postes

## ✅ Checklist de Configuration

Avant le déploiement en production, assurez-vous de:

- [ ] Générer une nouvelle SECRET_KEY sécurisée
- [ ] Configurer DEBUG=False
- [ ] Ajouter votre domaine dans ALLOWED_HOSTS et CSRF_TRUSTED_ORIGINS
- [ ] Configurer PostgreSQL et DATABASE_URL
- [ ] Configurer AWS Lightsail Object Storage (bucket + clés)
- [ ] Configurer l'email SMTP (SendGrid/SES)
- [ ] Mettre à jour les informations de contact (téléphone, email, adresse)
- [ ] Remplacer les "XXX FC" par les vrais prix
- [ ] Ajouter le lien Google Maps
- [ ] Configurer les comptes réseaux sociaux
- [ ] Tester l'upload de CV
- [ ] Tester les notifications email
- [ ] Configurer SSL (Let's Encrypt)
- [ ] Créer des postes d'emploi dans l'admin

## 🎨 Personnalisation

### Couleurs de la marque (dans base.html)

- Navy: `#003B5C`
- Orange: `#E76F51`
- Orange clair: `#F4A261`
- Jaune: `#F6BD60`
- Cyan: `#2A9D8F`
- Cyan clair: `#3AACB8`

### Logo

Remplacez `static/images/logo.png` par votre logo.

## 📱 Contact Support

Pour toute question ou problème:
- Email: contact@shinecongo.com
- GitHub Issues: [votre-repo/issues]

## 📄 Licence

© 2024 Shine Congo. Tous droits réservés.
