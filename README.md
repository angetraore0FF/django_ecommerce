# 🛍️ KaderShop - Plateforme E-commerce

Une plateforme e-commerce moderne développée avec Django, proposant une expérience d'achat complète avec système de vendeurs multiples.

## ✨ Fonctionnalités

### 🎯 Pour les clients
- **Navigation avancée** : Recherche, filtres par catégorie, tri par prix
- **Panier intelligent** : Gestion des quantités, codes promo, livraison calculée
- **Système de favoris** : Sauvegarde des produits préférés
- **Avis et notations** : Système de modération automatique
- **Commandes sécurisées** : Suivi du statut, historique détaillé
- **Compte personnel** : Profil, confirmation email, mot de passe

### 🏪 Pour les vendeurs
- **Dashboard complet** : Vue d'ensemble des ventes et statistiques
- **Gestion des produits** : Ajout, modification, gestion du stock
- **Suivi des commandes** : Traitement et mise à jour du statut
- **Analytics** : Graphiques de ventes, revenus, produits populaires

### ⚙️ Fonctionnalités techniques
- **Design responsive** : Compatible mobile, tablette, desktop
- **Interface moderne** : Design inspiré Apple, animations fluides
- **Sécurité renforcée** : Authentification, confirmation email, CSRF protection
- **Performance optimisée** : Requêtes SQL efficaces, pagination

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip
- virtualenv (recommandé)

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/votre-username/kadershop.git
   cd kadershop

python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver 8080
