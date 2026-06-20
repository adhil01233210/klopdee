from django.db import models

# Create your models here.
class UserRegister(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)
    age = models.IntegerField()
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    user = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE,
        related_name="products"
    )

    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.product_name}"