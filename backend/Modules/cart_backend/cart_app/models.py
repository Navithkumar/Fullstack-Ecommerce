from django.db import models


class Cart(models.Model):

  product = models.IntegerField()
  user = models.IntegerField()
  quantity = models.PositiveIntegerField()
  cart_price =  models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"User {self.user_id} - Product {self.product_id} ({self.quantity})"