from django.db import models

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.IntegerField()
    category_id = models.IntegerField()  
    product_image = models.FileField(upload_to='product_image/')
    product_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name}"


class ProductSpecification(models.Model):
    
    product = models.ForeignKey('Products',
    on_delete=models.SET_NULL,null=True,
    blank=True,related_name='specifications')

    product_colour = models.CharField(max_length=100)
    product_size = models.CharField(max_length=100)
    product_model_name = models.CharField(max_length=100)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product_colour}"

class ProductInventory(models.Model):
    
    product = models.ForeignKey('Products',
    on_delete=models.SET_NULL,null=True,
    blank=True,related_name='inventory')
    product_stock_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_stock_count}"