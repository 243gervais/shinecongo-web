#!/bin/bash

# Shine Congo - Quick Start Script
# Ce script initialise rapidement le projet pour le développement local

echo "🚗 Shine Congo - Quick Start"
echo "=============================="
echo ""

# Vérifier si nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Exécutez ce script depuis la racine du projet."
    exit 1
fi

# Vérifier si venv existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer venv
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Vérifier si .env existe
if [ ! -f ".env" ]; then
    echo "⚙️  Création du fichier .env pour le développement..."
    cat > .env << EOF
# Development Settings
SECRET_KEY=dev-secret-key-$(openssl rand -hex 32)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Database - Empty for SQLite
DATABASE_URL=

# Email Settings (optional for dev)
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@shinecongo.local
ADMIN_EMAIL=admin@shinecongo.local

# AWS S3 (optional for dev - uses local media folder)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
AWS_S3_ENDPOINT_URL=
EOF
    echo "✅ Fichier .env créé avec des valeurs par défaut"
fi

# Migrations
echo "🔄 Application des migrations..."
python manage.py migrate --no-input

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --no-input

# Vérifier si superuser existe
echo ""
read -p "Voulez-vous créer un superutilisateur? (o/n): " create_super
if [ "$create_super" = "o" ] || [ "$create_super" = "O" ]; then
    python manage.py createsuperuser
fi

# Demander si on doit créer des données d'exemple
echo ""
read -p "Voulez-vous créer des postes d'emploi d'exemple? (o/n): " create_sample
if [ "$create_sample" = "o" ] || [ "$create_sample" = "O" ]; then
    echo "📊 Création des données d'exemple..."
    python manage.py shell < init_sample_data.py
fi

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "🚀 Pour démarrer le serveur de développement:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "📍 URLs importantes:"
echo "   Site:  http://localhost:8000"
echo "   Admin: http://localhost:8000/admin"
echo ""
echo "📖 Consultez README.md pour plus d'informations"
echo ""
