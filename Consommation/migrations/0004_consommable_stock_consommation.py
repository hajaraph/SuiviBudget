# Generated by Django 5.1.2 on 2024-10-22 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Consommation', '0003_utilisateur_id_alter_utilisateur_nom_utilisateur_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consommable',
            fields=[
                ('id_consommable', models.AutoField(primary_key=True, serialize=False)),
                ('nom_consommable', models.CharField(max_length=80)),
                ('categorie', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id_stock', models.AutoField(primary_key=True, serialize=False)),
                ('quantite_stock', models.IntegerField(default=0)),
                ('date_maj_stock', models.DateField(auto_now=True)),
                ('consommable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Consommation.consommable')),
            ],
        ),
        migrations.CreateModel(
            name='Consommation',
            fields=[
                ('id_conso', models.AutoField(primary_key=True, serialize=False)),
                ('date_conso', models.DateField(auto_now=True)),
                ('quantite_conso', models.IntegerField(default=0)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Consommation.stock')),
            ],
        ),
    ]