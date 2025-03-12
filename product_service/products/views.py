from rest_framework import generics, filters
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inventory']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'