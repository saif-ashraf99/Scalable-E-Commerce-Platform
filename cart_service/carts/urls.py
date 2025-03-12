from django.urls import path
from .views import cart_operations, clear_cart

urlpatterns = [
    path('', cart_operations, name='cart-operations'),
    path('clear/', clear_cart, name='clear-cart'),
]