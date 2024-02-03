from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from home.models import SoftDeleteModel, SoftDeleteQuerySet                                                                                     
from django.db import models
from products.models import Product, ProductVariation


phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Invalid phone number.")


class MyUserManager(BaseUserManager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(MyUserManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model).filter(deleted=None)
        return SoftDeleteQuerySet(self.model)

    def delete(self):    
        return self.get_queryset().delete()  

    def hard_delete(self):
        return self.get_queryset().hard_delete()    
    
    def restore(self):
        return self.get_queryset().restore()    

    def create_user(self, full_name, email, phone=None, password=None):
        if not full_name:
            raise ValueError('Full name is required')
        if not email:
            raise ValueError('Email is required')       

        user = self.model(full_name=full_name, phone=phone, email=email, password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, phone=None, password=None):
        user = self.create_user(full_name=full_name, email=email, phone=phone,  password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, SoftDeleteModel):
    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, validators=[phone_regex], null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = MyUserManager()

    class Meta:
        verbose_name_plural = 'Users'
        ordering = ['-created']   

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True   


class Address(SoftDeleteModel):
    TYPE_CHOICES = (
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Others', 'Others'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    address = models.TextField(max_length=300)
    locality = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)   

    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['-created']   

    def __str__(self):
        return self.user.full_name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="wish_users")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wish_products')
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, blank=True, related_name='wish_variations')

    def __str__(self):
        return self.user.full_name
