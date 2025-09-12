from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    role = models.IntegerField()
    status = models.IntegerField()
    
    class Meta:
        managed = False                 
        db_table = "my_app_user" 

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User,
    on_delete=models.SET_NULL,null=True,
    blank=True,related_name='products')
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

class ProductsInventory(models.Model):
    
    stock_count = models.IntegerField()
    product = models.ForeignKey('Products',
    on_delete=models.SET_NULL,null=True,
    blank=True,related_name='inventory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock_count}"