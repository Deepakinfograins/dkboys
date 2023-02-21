from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import (
    UserManager
)


class User(AbstractUser):
    username = models.CharField(max_length=50,unique=True)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_verified =models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True,blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects=UserManager()

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return str(self.email)




class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=255)
    locality=models.CharField(_("locality"), max_length=255)
    city=models.CharField(_("city"), max_length=150)
    zipcode=models.IntegerField(_("zipcode"))
    state=models.CharField(_("state"),max_length=255)
    
    class Meta:
        verbose_name_plural = "Customer"


    def __str__(self):
        return str(self.id)
    
    


class Category(models.Model):
    category=models.CharField(_("category"), max_length=150)
    def __str__(self):
        return str(self.category)




class Product(models.Model):
    title=models.CharField(_("title"), max_length=150)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    discription=models.TextField(_("discription"))
    brand=models.CharField(_("brand"),max_length=255)
    category=models.ForeignKey(Category, related_name='pro_cat',on_delete=models.CASCADE)
    product_image=models.ImageField(_("product_image"), upload_to='producting')
    
    class Meta:
        verbose_name_plural = "Product"

    def __str__(self):
        return str(self.title)


    
 
    
class Cart(models.Model):
    user=models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    product=models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(_("quantity"),default=1)
    
    class Meta:
        verbose_name_plural = "Cart"


    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
status_choices=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)
class OrderPlace(models.Model):
    user=models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, verbose_name=_("customer"), on_delete=models.CASCADE)
    product=models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(_("quantity"),default=1)
    ordered_date=models.DateTimeField(_("ordered_date"), auto_now_add=True)
    status=models.CharField(_("status"),choices= status_choices,max_length=50,default='Pending')
    
    class Meta:
        verbose_name_plural = "OrderPlace"
    
    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

class ProductImages(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    multiple_image=models.ImageField(upload_to='multiple_image')

    class Meta:
        verbose_name_plural = "ProductImages"
    

    def __str__(self):
        return str(self.product)


class Banner(models.Model):
    banner=models.ImageField(upload_to='banner')

    class Meta:
        verbose_name_plural = "Banner"

    def __str__(self):
        return str(self.banner)
  
        