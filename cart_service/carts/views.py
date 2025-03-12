from django_redis import get_redis_connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_operations(request):
    user_id = request.user.id
    redis = get_redis_connection("default")
    cart_key = f'cart:{user_id}'
    
    if request.method == 'GET':
        items = redis.hgetall(cart_key)
        return Response({
            'user_id': user_id,
            'items': {k.decode(): int(v.decode()) for k, v in items.items()}
        })
    
    if request.method == 'POST':
        product_id = str(request.data.get('product_id'))
        quantity = int(request.data.get('quantity', 1))
        
        # Validate product exists (call Product Service)
        current_quantity = redis.hincrby(cart_key, product_id, quantity)
        return Response({
            'product_id': product_id,
            'quantity': current_quantity
        }, status=status.HTTP_201_CREATED)
    
    if request.method == 'PUT':
        product_id = str(request.data.get('product_id'))
        quantity = int(request.data.get('quantity', 1))
        
        if quantity <= 0:
            redis.hdel(cart_key, product_id)
            return Response({'status': 'item removed'})
        
        redis.hset(cart_key, product_id, quantity)
        return Response({'product_id': product_id, 'quantity': quantity})
    
    if request.method == 'DELETE':
        product_id = str(request.data.get('product_id'))
        redis.hdel(cart_key, product_id)
        return Response({'status': 'item removed'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    user_id = request.user.id
    redis = get_redis_connection("default")
    redis.delete(f'cart:{user_id}')
    return Response({'status': 'cart cleared'})