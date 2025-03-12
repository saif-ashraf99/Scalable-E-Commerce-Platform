from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'total', 'status', 'created_at', 'items']
        read_only_fields = ['total', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        # Calculate total and create items
        total = 0
        for item_data in items_data:
            # In production: Validate product exists and get price from Product Service
            item = OrderItem.objects.create(order=order, **item_data)
            total += item.quantity * item.price
        
        order.total = total
        order.save()
        return order