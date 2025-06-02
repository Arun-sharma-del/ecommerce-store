from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import checkout


urlpatterns = [
    path('', views.index, name='index'),path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', views.register, name ='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('accounts/profile/', views.profile_view, name = 'profile'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    
]

