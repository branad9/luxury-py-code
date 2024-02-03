from django.db import models
from users.models import User
from products.models import Product, ProductVariation


class Order(models.Model):
    ORDER_STATUS = (
        ("Ordered", "Ordered"),
        ("Shipped", "Shipped"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=250, null=True, blank=True)
    order_note = models.CharField(max_length=250, null=True, blank=True)
    order_total = models.DecimalField(max_digits=20, decimal_places=2)
    delivery_charges = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )
    track_number = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default="Ordered")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cancelled_by",
    )
    cancellation_reason = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ["-created"]

    def __str__(self):
        return self.user.full_name


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderitems"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, null=True, blank=True
    )
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Order Items"
        ordering = ["-created"]

    def __str__(self):
        return self.product.name
