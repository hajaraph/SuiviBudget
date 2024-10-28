from django.contrib.auth.models import AbstractUser
from django.db import models

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    nom_service = models.CharField(max_length=80)


class Utilisateur(AbstractUser):
    nom_utilisateur = models.CharField(max_length=50, unique=True)
    numero_utilisateur = models.CharField(max_length=10, unique=True)
    est_admin = models.BooleanField(default=False)

    first_name = None
    last_name = None
    groups = None
    user_permissions = None
    is_staff = None
    is_superuser = None
    email = None
    username = None

    USERNAME_FIELD = 'nom_utilisateur'
    SUPERUSER_FIELD = 'est_admin'

    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)


class Consommable(models.Model):
    id_consommable = models.AutoField(primary_key=True)
    nom_consommable = models.CharField(max_length=80)
    categorie = models.CharField(max_length=80)


class Stock(models.Model):
    id_stock = models.AutoField(primary_key=True)
    quantite_stock = models.IntegerField(default=0)
    date_maj_stock = models.DateField(auto_now=True)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)


class Consommation(models.Model):
    id_conso = models.AutoField(primary_key=True)
    date_conso = models.DateField(auto_now=True)
    quantite_conso = models.IntegerField(default=0)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
