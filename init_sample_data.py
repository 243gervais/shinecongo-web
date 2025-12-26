#!/usr/bin/env python
"""
Script d'initialisation pour créer des données d'exemple pour Shine Congo.
Exécuter avec: python manage.py shell < init_sample_data.py
"""

from careers.models import JobRole

print("🚀 Création des postes d'exemple pour Shine Congo...")

# Vérifier si des postes existent déjà
if JobRole.objects.exists():
    print("⚠️  Des postes existent déjà. Voulez-vous continuer? (y/n)")
    response = input().lower()
    if response != 'y':
        print("❌ Annulé.")
        exit()

# Créer les postes d'exemple
jobs = [
    {
        "title": "Laveur de Voitures",
        "slug": "laveur-de-voitures",
        "description": """Shine Congo recherche des laveurs de voitures motivés et professionnels pour rejoindre notre équipe dynamique. 

Vous serez formé à nos méthodes de lavage premium et utiliserez des équipements modernes pour garantir la satisfaction de nos clients.""",
        "responsibilities": """• Effectuer le lavage extérieur complet des véhicules
• Assurer l'aspiration et le nettoyage intérieur
• Nettoyer les vitres et miroirs
• Traiter les pneus et jantes
• Maintenir la propreté de la zone de travail
• Respecter les procédures de qualité et de sécurité
• Offrir un service client excellent""",
        "requirements": """• Motivation et volonté d'apprendre
• Bonne condition physique
• Sens du détail et souci de la qualité
• Ponctualité et fiabilité
• Bon relationnel avec les clients
• Aucune expérience préalable requise (formation fournie)
• Niveau primaire minimum""",
        "benefits": """• Formation complète aux techniques de lavage professionnel
• Salaire mensuel de XXX FC + primes de performance
• Uniformes fournis
• Horaires fixes (8h-17h, du lundi au samedi)
• Possibilité d'évolution vers superviseur
• Environnement de travail moderne
• Équipe jeune et dynamique""",
        "employment_type": "FULL_TIME",
    },
    {
        "title": "Technicien Detailing",
        "slug": "technicien-detailing",
        "description": """Nous recherchons un technicien detailing expérimenté pour notre service premium. Si vous êtes passionné par l'esthétique automobile et avez un œil pour les détails, ce poste est fait pour vous!""",
        "responsibilities": """• Effectuer le detailing complet des véhicules (intérieur et extérieur)
• Polissage et correction de peinture
• Application de traitements céramiques
• Nettoyage et traitement du cuir
• Traitement des plastiques et des vitres
• Conseiller les clients sur l'entretien de leur véhicule
• Gérer les produits et équipements de detailing""",
        "requirements": """• Minimum 2 ans d'expérience en detailing automobile
• Maîtrise des techniques de polissage
• Connaissance des produits professionnels
• Perfectionniste avec excellent souci du détail
• Capacité à travailler de manière autonome
• Bonne présentation et communication
• Diplôme secondaire ou équivalent""",
        "benefits": """• Salaire attractif (XXX FC/mois) selon expérience
• Accès aux meilleurs équipements et produits
• Formation continue sur les nouvelles techniques
• Primes basées sur la satisfaction client
• Horaires flexibles possibles
• Opportunité de travailler sur des véhicules premium
• Possibilité d'évolution vers Chef Detailing""",
        "employment_type": "FULL_TIME",
    },
    {
        "title": "Superviseur d'Équipe",
        "slug": "superviseur-equipe",
        "description": """Shine Congo cherche un superviseur d'équipe pour coordonner nos opérations quotidiennes et assurer que nos standards de qualité élevés sont maintenus. Vous serez le leader d'une équipe de 10-15 personnes.""",
        "responsibilities": """• Superviser et coordonner l'équipe de laveurs
• Assurer le respect des standards de qualité Shine Congo
• Planifier et organiser les tâches quotidiennes
• Former les nouveaux employés
• Gérer les stocks de produits et matériel
• Résoudre les problèmes et réclamations clients
• Faire rapport à la direction
• Maintenir un environnement de travail sûr et productif""",
        "requirements": """• Minimum 3 ans d'expérience dans le lavage auto ou service similaire
• Au moins 1 an d'expérience en supervision d'équipe
• Excellentes compétences en leadership et communication
• Capacité à former et motiver une équipe
• Orientation résultats et qualité
• Compétences organisationnelles
• Diplôme secondaire ou équivalent
• Maîtrise du français (anglais est un plus)""",
        "benefits": """• Salaire compétitif (XXX FC/mois)
• Bonus trimestriel basé sur la performance
• Formation en management
• Possibilité d'évolution vers Directeur des Opérations
• Assurance santé après période d'essai
• Téléphone professionnel fourni
• Congés payés
• Environnement de travail moderne""",
        "employment_type": "FULL_TIME",
    },
    {
        "title": "Réceptionniste / Caissier(ère)",
        "slug": "receptionniste-caissier",
        "description": """Nous recherchons une personne souriante, organisée et professionnelle pour gérer l'accueil de nos clients et les transactions. Vous serez le premier contact de nos clients avec Shine Congo.""",
        "responsibilities": """• Accueillir chaleureusement les clients
• Enregistrer les demandes de service et créer les tickets
• Gérer les paiements (cash, mobile money, etc.)
• Répondre aux questions des clients
• Gérer les appels téléphoniques et WhatsApp
• Tenir la caisse et effectuer les rapports quotidiens
• Coordonner avec l'équipe de lavage
• Maintenir la zone d'accueil propre et organisée""",
        "requirements": """• Diplôme secondaire minimum
• Expérience en service client (1 an minimum)
• Excellente présentation et communication
• Capacités en mathématiques de base
• Maîtrise du français (lingala est un plus)
• Compétences informatiques de base
• Ponctualité et fiabilité
• Souriant(e) et orienté(e) client""",
        "benefits": """• Salaire mensuel: XXX FC
• Primes mensuelles basées sur la performance
• Formation continue en service client
• Horaires: 8h-17h (du lundi au samedi)
• Environnement de travail climatisé
• Uniformes fournis
• Possibilité d'évolution vers Responsable Clientèle
• Équipe sympathique et professionnelle""",
        "employment_type": "FULL_TIME",
    },
]

# Créer les postes
created_count = 0
for job_data in jobs:
    job, created = JobRole.objects.get_or_create(
        slug=job_data['slug'],
        defaults=job_data
    )
    if created:
        created_count += 1
        print(f"✅ Créé: {job.title}")
    else:
        print(f"ℹ️  Existant: {job.title}")

print(f"\n🎉 Terminé! {created_count} poste(s) créé(s).")
print(f"📊 Total des postes actifs: {JobRole.objects.filter(is_active=True).count()}")
print("\n👉 Vous pouvez maintenant accéder à l'admin pour modifier ces postes:")
print("   http://localhost:8000/admin/careers/jobrole/")
