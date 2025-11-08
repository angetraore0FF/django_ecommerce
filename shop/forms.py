from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, Product
from django.core.exceptions import ValidationError
import re
from .models import Order, ProductReview # Assurez-vous que ProductReview est bien importé

class CartAddProductForm(forms.Form):
    """
    Formulaire pour ajouter des produits au panier
    """
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;'
        })
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

class OrderCreateForm(forms.ModelForm):
    """
    Formulaire pour créer une commande
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code postal'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse email',
            'address': 'Adresse',
            'postal_code': 'Code postal', 
            'city': 'Ville',
        }

# Dans forms.py - Modifiez la classe CustomUserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom'
        })
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'JJ/MM/AAAA'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+33 6 12 34 56 78'
        })
    )
    # ✅ NOUVEAU CHAMP : Devenir vendeur
    become_vendor = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label="Devenir vendeur sur KaderShop"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'phone_number', 'password1', 'password2', 'become_vendor']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un compte avec cet email existe déjà.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^[\+]?[0-9\s\-\(\)]{10,15}$', phone_number):
            raise ValidationError("Veuillez entrer un numéro de téléphone valide.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
    
        if commit:
            user.save()
        
        # Créer le profil utilisateur
        from .models import UserProfile
        UserProfile.objects.create(
            user=user,
            birth_date=self.cleaned_data['birth_date'],
            phone_number=self.cleaned_data['phone_number'],
            email_confirmed=False,
            # ✅ ENREGISTRER LE CHOIX "DEVENIR VENDEUR"
            wants_to_be_vendor=self.cleaned_data['become_vendor']
        )
        return user

# ✅ NOUVEAU FORMULAIRE POUR LES AVIS
class ProductReviewForm(forms.ModelForm):
    """Formulaire pour les avis produits avec filtres automatiques"""
    
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} étoile(s)') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre avis'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez votre expérience avec ce produit...',
                'rows': 4
            }),
        }
        labels = {
            'rating': 'Note',
            'title': 'Titre',
            'comment': 'Commentaire',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # ✅ Récupère l'utilisateur
        super().__init__(*args, **kwargs)
    
    def clean_title(self):
        """Filtre pour le titre"""
        title = self.cleaned_data.get('title')
        
        # Liste de mots inappropriés
        inappropriate_words = ['spam', 'arnaque', 'escroc', 'merde', 'con', 'connard', 'pute', 'salope']
        
        # Vérifier la longueur
        if len(title) < 5:
            raise ValidationError("Le titre doit contenir au moins 5 caractères.")
        
        if len(title) > 100:
            raise ValidationError("Le titre ne peut pas dépasser 100 caractères.")
        
        # Vérifier les mots inappropriés
        for word in inappropriate_words:
            if word in title.lower():
                raise ValidationError("Le titre contient des mots inappropriés.")
        
        return title
    
    def clean_comment(self):
        """Filtre pour le commentaire"""
        comment = self.cleaned_data.get('comment')
        
        # Liste de mots inappropriés
        inappropriate_words = [
    # Mots existants (Nettoyage de base)
    'spam', 'arnaque', 'escroc', 
    
    # Insultes/Vulgarité
    'merde', 'con', 'connard', 'pute', 'salope', 'putain', 
    'enculé', 'bâtard', 'abruti', 'idiot', 'débile', 'chienne', 
    'foutre', 'bordel',
    
    # Contenu sexuel/Nudité
    'nue', 'nude', 'sexe', 'viol', 'porn', 'porno', 'masturb', 'sodom', 'gode', 'bite', 'chatte', 'queue',
    
    # Violence/Haine/Menaces
    'violent', 'meutre', 'tuer', 'massacre', 'raciste', 'nazi', 'terror', 'haineux', 'frapper', 'suicide',
    
    # Substances illicites
    'drogue', 'coke', 'héroïne', 'crack', 'toxico',
    
    # Termes Financiers Trompeurs
    'gratuit', 'remboursement immédiat', 'sans risque', 'facile', 'rapide', # À utiliser avec prudence selon le contexte
]
        
        # Vérifier la longueur
        if len(comment) < 10:
            raise ValidationError("Le commentaire doit contenir au moins 10 caractères.")
        
        if len(comment) > 1000:
            raise ValidationError("Le commentaire ne peut pas dépasser 1000 caractères.")
        
        # Vérifier les mots inappropriés
        for word in inappropriate_words:
            if word in comment.lower():
                raise ValidationError("Le commentaire contient des mots inappropriés.")
        
        # Vérifier le ratio majuscules/minuscules (éviter les cris)
        if len(comment) > 20:
            uppercase_count = sum(1 for c in comment if c.isupper())
            if uppercase_count / len(comment) > 0.5:
                raise ValidationError("Veuillez éviter d'écrire en majuscules.")
        
        return comment
    
    def clean_rating(self):
        """Filtre pour la note"""
        rating = self.cleaned_data.get('rating')
        
        # ✅ CORRECTION : Vérifier si l'utilisateur est disponible
        if self.user and self.user.is_authenticated:
            # Vérifier les notes extrêmes (1 ou 5) pour les nouveaux utilisateurs
            user_reviews = ProductReview.objects.filter(user=self.user)
            if user_reviews.count() < 3 and rating in [1, 5]:
                # Pour les nouveaux utilisateurs, demander un commentaire plus détaillé
                comment = self.cleaned_data.get('comment', '')
                if len(comment) < 50:
                    raise ValidationError(
                        "Pour les notes extrêmes (1 ou 5 étoiles), veuillez fournir "
                        "un commentaire détaillé d'au moins 50 caractères expliquant votre évaluation."
                    )
        
        return rating

# ✅ NOUVEAU FORMULAIRE POUR LES COUPONS
class CouponApplyForm(forms.Form):
    """Formulaire pour appliquer un code promo"""
    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre code promo',
            'style': 'text-transform: uppercase;'
        }),
        label="Code promo"
    )
    
    def clean_code(self):
        """Normalise le code promo en majuscules et sans espaces inutiles"""
        code = self.cleaned_data.get('code').upper().strip()
        return code
    
# ✅ AJOUTEZ CE FORMULAIRE À LA FIN DE shop/forms.py

class ProductForm(forms.ModelForm):
    """Formulaire pour la gestion des produits par les vendeurs"""
    
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'price', 'image', 'stock', 'available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du produit'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'slug-automatique-ou-personnalise'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description détaillée du produit...',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantité en stock'
            }),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nom du produit',
            'slug': 'Slug (URL)',
            'description': 'Description',
            'price': 'Prix (€)',
            'image': 'Image du produit',
            'stock': 'Stock disponible',
            'available': 'Produit disponible',
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError("Le prix doit être supérieur à 0.")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise ValidationError("Le stock ne peut pas être négatif.")
        return stock