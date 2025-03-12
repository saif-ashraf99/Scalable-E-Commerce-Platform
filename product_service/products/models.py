from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    inventory = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.name} (${self.price})"