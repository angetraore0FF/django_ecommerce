🛍️ KaderShop - Plateforme E-Commerce Django

Une plateforme e-commerce moderne et complète développée avec Django, offrant une expérience d'achat complète avec gestion des produits, panier, commandes, système d'avis, codes promo, et espace vendeur.

✨ Fonctionnalités

🎯 Fonctionnalités Principales
- Catalogue Produits : Navigation par catégories, recherche et tri
- Gestion Panier : Ajout, modification, suppression d'articles
- Processus de Commande : Validation de stock, calcul automatique des prix
- Système d'Authentication : Inscription, connexion, confirmation email
- Profils Utilisateurs : Gestion des informations personnelles et historique

⭐ Fonctionnalités Avancées
- 🔄 Codes Promo : Pourcentage, montant fixe, livraison gratuite avec restrictions
- ❤️ Favoris : Liste de souhaits personnalisée
- ⭐ Avis & Notes : Système de modération automatique et manuelle
- 👥 Espace Vendeur : Dashboard, gestion produits, statistiques de vente
- 📧 Service Email : Confirmation de compte, notifications

🛠️ Administration
- Interface Admin Django enrichie avec actions personnalisées
- Modération des avis avec filtres intelligents
- Gestion des coupons avec statistiques d'utilisation
- Tableaux de bord pour le suivi des performances

🚀 Installation

Prérequis
- Python 3.8+
- Django 5.2+
- Pillow (gestion des images)

Installation

1. Cloner le repository

git clone https://github.com/angetraore0FF/django_ecommerce.git
cd django_ecommerce

2. Créer une environnement virtuel
   
   python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows 

3.Installer les dépendances

pip install -r requirements.txt

4.Configuration de la base de données

python manage.py makemigrations
python manage.py migrate

5.Créer un superutilisateur

python manage.py createsuperuser

6.Lancer le serveur de développement

python manage.py runserver
