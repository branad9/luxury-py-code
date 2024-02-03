from django.db import models
from users.models import User
from products.models import Product, ProductVariation


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, blank=True, related_name='variations')
    total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    qty = models.IntegerField()
    created = models.DateTimeField(null=True, auto_now_add=True)
    updated = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Cart Items'

    def sub_total(self):
        if self.product.sale_price is not None:
            return self.product.sale_price * self.qty
        else:
            return self.product.price * self.qty
        