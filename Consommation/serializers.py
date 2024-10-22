from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from Consommation.models import Service

Utilisateur = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Utilisateur
        fields = ('nom_utilisateur', 'password', 'password_confirm', 'est_admin', 'numero_utilisateur', 'service')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Les mots de passe ne correspondent pas.'})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        # Créer l'utilisateur
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
        fields = ('nom_service',)

    def create(self, validated_data):
        return Service.objects.create(
            nom_service=validated_data['nom_service'],
        )

    def update(self, instance, validated_data):
        instance.nom_service = validated_data.get('nom_service', instance.nom_service)
        instance.save()
        return instance

