from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user_id = models.IntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_item'

    def __str__(self):
        return f"{self.quantity}x Product {self.product_id} @ {self.price}"