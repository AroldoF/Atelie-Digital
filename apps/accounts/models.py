from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from apps.utils.storage import profile_image_upload_path


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("O usuário precisa ter um username")
        if not email:
            raise ValueError("O usuário precisa ter um email")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True, max_length=255)
    cpf = models.CharField(unique=True, max_length=11)
    phone_number = models.CharField(unique=True, max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    is_artisan = models.BooleanField(default=False)

    # campos obrigatórios
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"  # login por username
    REQUIRED_FIELDS = ["email"]  # exigido ao criar superuser

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=profile_image_upload_path)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "profiles"


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE
    )
    complement = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    street = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.street}, Nº {self.number}. {self.city}'

    class Meta:
        db_table = "addresses"
