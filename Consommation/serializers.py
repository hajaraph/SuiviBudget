from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

Utilisateur = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True),

    class Meta:
        model = Utilisateur
        fields = ('nom_utilisateur', 'password', 'password_confirm', 'est_admin', 'numero_utilisateur', 'service_id')

        @staticmethod
        def validate(attrs):
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError({'password': 'Les mots de passe ne correspondent pas'})
            return attrs

        @staticmethod
        def create(validated_data):
            validated_data.pop('password_confirm')

            utilisateur = Utilisateur.objects.create(
                nom_utilisateur=validated_data['nom_utilisateur'],
                est_admin=validated_data['est_admin'],
                numero_utilisateur=validated_data['numero_utilisateur'],
                service_id=validated_data['service_id']
            )
            utilisateur.set_password(validated_data['password'])
            utilisateur.save()
            return utilisateur
