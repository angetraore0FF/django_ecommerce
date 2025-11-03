from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Product, Category, Order, OrderItem
from .forms import ProductForm

# Decorator personnalisé pour vérifier si l'utilisateur est vendeur
# Dans vendors.py - Améliorez le décorateur vendor_required

def vendor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Veuillez vous connecter pour accéder à l'espace vendeur.")
            return redirect('shop:login')
        
        # ✅ MODIFICATION : Autoriser aussi les utilisateurs qui souhaitent devenir vendeur
        is_vendor = (
            hasattr(request.user, 'profile') and 
            (request.user.vendor_products.exists() or 
             request.user.profile.wants_to_be_vendor)
        )
        
        if not is_vendor and not request.user.is_staff:
            messages.error(request, "Accès réservé aux vendeurs.")
            return redirect('shop:product_list')
            
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@vendor_required
def vendor_dashboard(request):
    """Tableau de bord du vendeur"""
    vendor_products = Product.objects.filter(vendor=request.user)
    
    # Statistiques
    total_products = vendor_products.count()
    total_sales = OrderItem.objects.filter(
        product__vendor=request.user,
        order__paid=True
    ).aggregate(total=Sum('price'))['total'] or 0
    
    # Commandes récentes
    recent_orders = OrderItem.objects.filter(
        product__vendor=request.user
    ).select_related('order', 'product').order_by('-order__created')[:10]
    
    # Produits les plus vendus
    top_products = OrderItem.objects.filter(
        product__vendor=request.user
    ).values('product__name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]
    
    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'vendor_products': vendor_products,
    }
    
    return render(request, 'vendors/dashboard.html', context)

@login_required
@vendor_required
def vendor_products(request):
    """Liste des produits du vendeur"""
    products = Product.objects.filter(vendor=request.user).order_by('-created')
    
    return render(request, 'vendors/products/list.html', {
        'products': products
    })

@login_required
@vendor_required
def vendor_add_product(request):
    """Ajouter un nouveau produit"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user  # Assigner le vendeur
            product.save()
            messages.success(request, "Produit ajouté avec succès !")
            return redirect('shop:vendor_products')
    else:
        form = ProductForm()
    
    return render(request, 'vendors/products/add.html', {
        'form': form,
        'categories': Category.objects.all()
    })

@login_required
@vendor_required
def vendor_edit_product(request, product_id):
    """Modifier un produit existant"""
    product = get_object_or_404(Product, id=product_id, vendor=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifié avec succès !")
            return redirect('shop:vendor_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'vendors/products/edit.html', {
        'form': form,
        'product': product
    })

@login_required
@vendor_required
def vendor_orders(request):
    """Commandes des produits du vendeur"""
    status_filter = request.GET.get('status', 'all')
    
    order_items = OrderItem.objects.filter(product__vendor=request.user)
    
    if status_filter != 'all':
        order_items = order_items.filter(order__status=status_filter)
    
    order_items = order_items.select_related('order', 'product').order_by('-order__created')
    
    return render(request, 'vendors/orders/list.html', {
        'order_items': order_items,
        'status_filter': status_filter
    })

@login_required
@vendor_required
def vendor_order_detail(request, order_id):
    """Détail d'une commande"""
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(
        order=order,
        product__vendor=request.user
    )
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Statut de la commande mis à jour : {order.get_status_display()}")
    
    return render(request, 'vendors/orders/detail.html', {
        'order': order,
        'order_items': order_items
    })

@login_required
@vendor_required
def vendor_earnings(request):
    """Revenus du vendeur"""
    period = request.GET.get('period', 'month')
    today = timezone.now().date()
    
    if period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today - timedelta(days=30)
    elif period == 'year':
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=30)
    
    # Calcul des revenus
    earnings = OrderItem.objects.filter(
        product__vendor=request.user,
        order__paid=True,
        order__created__date__gte=start_date
    ).annotate(
        total_earning=Sum('price')
    ).order_by('-order__created')
    
    total_earned = OrderItem.objects.filter(
        product__vendor=request.user,
        order__paid=True,
        order__created__date__gte=start_date
    ).aggregate(total=Sum('price'))['total'] or 0
    
    context = {
        'earnings': earnings,
        'total_earned': total_earned,
        'period': period,
    }
    
    return render(request, 'vendors/earnings/list.html', context)

# API pour les statistiques
@login_required
@vendor_required
def vendor_sales_statistics_api(request):
    """API pour les statistiques de vente"""
    period = request.GET.get('period', '7')
    days = int(period)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    dates = [start_date + timedelta(days=x) for x in range(days + 1)]
    
    sales_data = []
    for date in dates:
        daily_sales = OrderItem.objects.filter(
            product__vendor=request.user,
            order__paid=True,
            order__created__date=date
        ).aggregate(total=Sum('price'))['total'] or 0
        
        sales_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'sales': float(daily_sales)
        })
    
    return JsonResponse({'sales_data': sales_data})