from django.contrib.auth.models import AbstractUser
from django.db import models

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    nom_service = models.CharField(max_length=80)


class Utilisateur(AbstractUser):
    nom_utilisateur = models.CharField(max_length=50, primary_key=True)
    numero_utilisateur = models.CharField(max_length=10)
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
