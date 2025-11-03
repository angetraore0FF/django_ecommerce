from django.urls import path
from . import views
from . import vendors

app_name = 'shop'

urlpatterns = [
    # Pages produits
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Panier
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    
    # Commandes
    path('order/create/', views.order_create, name='order_create'),
    path('order/created/<int:order_id>/', views.order_created, name='order_created'),
    path('order/history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('coupon/apply/', views.apply_coupon, name='apply_coupon'),
    path('coupon/remove/', views.remove_coupon, name='remove_coupon'),
    
    # ✅ Favoris (Nouveauté)
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # ✅ Avis (Nouveauté)
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/report/', views.report_review, name='report_review'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('confirm-email/<uuid:token>/', views.confirm_email_view, name='confirm_email'),
    path('admin/confirm-email/<int:user_id>/', views.admin_confirm_email, name='admin_confirm_email'),
    path('resend-confirmation/', views.resend_confirmation_email, name='resend_confirmation'),

     # ✅ ESPACE VENDEUR
    path('vendor/dashboard/', vendors.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/products/', vendors.vendor_products, name='vendor_products'),
    path('vendor/products/add/', vendors.vendor_add_product, name='vendor_add_product'),
    path('vendor/products/edit/<int:product_id>/', vendors.vendor_edit_product, name='vendor_edit_product'),
    path('vendor/orders/', vendors.vendor_orders, name='vendor_orders'),
    path('vendor/orders/<int:order_id>/', vendors.vendor_order_detail, name='vendor_order_detail'),
    path('vendor/earnings/', vendors.vendor_earnings, name='vendor_earnings'),
    path('vendor/api/sales-statistics/', vendors.vendor_sales_statistics_api, name='vendor_sales_statistics_api'),
]