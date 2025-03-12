from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'inventory', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'price': {'min_value': 0.01},
            'inventory': {'min_value': 0}
        }