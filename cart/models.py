from django.db import models


from store.models import Product, Variation

# Create your models here.


class Cart(models.Model):
    # one-to-many
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id


class CartItem(models.Model):
    # One-To-Many
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Many-To-Many
    variations = models.ManyToManyField(Variation, blank=True)
    # Many-to-One
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def remove_item(self):
        quantity -= self.quantity

    def __unicode__(self) -> str:
        return self.product.product
