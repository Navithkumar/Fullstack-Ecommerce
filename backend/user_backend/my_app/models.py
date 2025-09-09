from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}"


class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, role=2, address=None, password=None, status=1):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            role=role,
            status=status,
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None):
        user = self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            role=1,
            status=1
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.IntegerChoices):
        ADMIN = 1, 'Admin'
        CUSTOMER = 2, 'Customer'
        SELLER = 3, 'Seller'

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.IntegerField(default=1)
    role = models.IntegerField(choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email