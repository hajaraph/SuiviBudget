from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Consommation.models import Service, Consommable, Stock, Consommation

Utilisateur = get_user_model()

# Serializer pour l'utilisateur
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Utilisateur
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Les mots de passe ne correspondent pas.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        utilisateur = Utilisateur.objects.create(
            nom_utilisateur=validated_data['nom_utilisateur'],
            numero_utilisateur=validated_data['numero_utilisateur'],
            service=validated_data['service'],
            est_admin=validated_data.get('est_admin', False)
        )

        # Hacher le mot de passe
        utilisateur.set_password(validated_data['password'])
        utilisateur.save()

        return utilisateur


class ServiceSerializer(serializers.ModelSerializer):
    nom_service = serializers.CharField(required=True)

    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        return Service.objects.create(
            nom_service=validated_data['nom_service'],
        )

    def update(self, instance, validated_data):
        instance.nom_service = validated_data.get('nom_service', instance.nom_service)
        instance.save()
        return instance


class ConsommableSerializer(serializers.ModelSerializer):
    nom_consommable = serializers.CharField(required=True)
    categorie = serializers.CharField(required=True)
    prix_unitaire = serializers.CharField(required=True)

    class Meta:
        model = Consommable
        fields = '__all__'

    def create(self, validated_data):
        return Consommable.objects.create(
            nom_consommable=validated_data['nom_consommable'],
            prix_unitaire=validated_data['prix_unitaire'],
            categorie=validated_data['categorie']
        )

    def update(self, instance, validated_data):
        instance.nom_consommable = validated_data.get('nom_consommable', instance.nom_consommable)
        instance.prix_unitaire = validated_data.get('prix_unitaire', instance.prix_unitaire)
        instance.categorie = validated_data.get('categorie', instance.categorie)
        instance.save()
        return instance


class StockSerializer(serializers.ModelSerializer):
    quantite_stock = serializers.IntegerField(required=True)
    consommable = serializers.PrimaryKeyRelatedField(
        queryset=Consommable.objects.all(),
        write_only=True
    )
    consommable_detail = ConsommableSerializer(source='consommable', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        quantite_stock = validated_data['quantite_stock']
        consommable = validated_data['consommable']
        utilisateur = validated_data['utilisateur']

        # Crée un stock ou met à jour la quantité de stock existante
        stock_up, created = Stock.objects.get_or_create(
            consommable=consommable,
            defaults={
                'quantite_stock': quantite_stock,
                'utilisateur': utilisateur
            }
        )

        if not created:
            stock_up.quantite_stock += quantite_stock
            stock_up.date_maj_stock = timezone.now()
            stock_up.utilisateur = utilisateur
            stock_up.save()

        return stock_up


class ConsommationSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        write_only=True
    )
    service_detail = ServiceSerializer(source="service", read_only=True)

    consommable = serializers.PrimaryKeyRelatedField(
        queryset=Consommable.objects.all(),
        write_only=True
    )
    consommable_detail = ConsommableSerializer(source="consommable", read_only=True)

    utilisateur = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.all(),
        write_only=True
    )
    utilisateur_detail = UserSerializer(source="utilisateur", read_only=True)

    stock_detail = StockSerializer(source="stock", read_only=True)  # Ajouter stock_detail ici

    class Meta:
        model = Consommation
        fields = (
            'id_conso', 'quantite_conso', 'date_conso', 'service', 'service_detail',
            'consommable', 'consommable_detail', 'utilisateur', 'utilisateur_detail', 'stock_detail'
        )

    def create(self, validated_data):
        quantite_conso = validated_data['quantite_conso']
        service = validated_data['service']
        consommable = validated_data['consommable']
        utilisateur = validated_data['utilisateur']

        # Récupérer le stock associé au consommable
        try:
            stock = Stock.objects.get(consommable=consommable)
        except Stock.DoesNotExist:
            raise ValidationError("Aucun stock associé à ce consommable.")

        # Vérification de la disponibilité du stock
        if stock.quantite_stock <= 0:
            raise ValidationError(f"Aucune quantité disponible dans le stock pour ce consommable.")

        # Vérification de la disponibilité du stock
        if stock.quantite_stock < quantite_conso:
            raise ValidationError(
                f"Stock insuffisant pour le consommable associé. "
                f"Quantité disponible : {stock.quantite_stock}, demandée : {quantite_conso}."
            )

        # Création ou mise à jour de la consommation
        conso, created = Consommation.objects.get_or_create(
            service=service,
            stock=stock,
            utilisateur=utilisateur,
            defaults={
                'quantite_conso': quantite_conso,
                'date_conso': timezone.now(),
            }
        )

        if not created:
            conso.quantite_conso += quantite_conso
            conso.save()

        # Mise à jour du stock
        stock.quantite_stock -= quantite_conso
        stock.date_maj_stock = timezone.now()
        stock.save()

        return conso
