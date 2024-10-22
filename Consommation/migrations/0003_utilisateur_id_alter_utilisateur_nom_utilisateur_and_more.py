# Generated by Django 5.1.2 on 2024-10-21 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Consommation", "0002_alter_utilisateur_service"),
    ]

    operations = [
        migrations.AddField(
            model_name="utilisateur",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=0,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="utilisateur",
            name="nom_utilisateur",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="utilisateur",
            name="numero_utilisateur",
            field=models.CharField(max_length=10, unique=True),
        ),
    ]