from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=200)
    cpf = models.CharField(unique=True, max_length=11)
    phone_number = models.CharField(unique=True, max_length=15)
    is_artisan = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

class Profiles(models.Model):
    user = models.OneToOneField(Users, related_name='profiles', on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'profiles'

class Addresses(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, related_name='addresses', on_delete=models.CASCADE)
    complement = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    street = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'