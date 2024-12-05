from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

Utilisateur = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Utilisateur
        fields = ('nom_utilisateur', 'password', 'password_confirm', 'est_admin', 'numero_utilisateur', 'service')

    def validate(self, attrs):
        # Vérification que les deux mots de passe correspondent
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Les mots de passe ne correspondent pas.'})

        return attrs

    def create(self, validated_data):
        # Supprimer le champ password_confirm avant la création de l'utilisateur
        validated_data.pop('password_confirm')

        # Créer l'utilisateur
        utilisateur = Utilisateur.objects.create(
            nom_utilisateur=validated_data['nom_utilisateur'],
            numero_utilisateur=validated_data['numero_utilisateur'],
            service=validated_data['service'],  # Utilisez 'service' et non 'service_id'
            est_admin=validated_data.get('est_admin', False)  # Utilisez la valeur par défaut ici
        )

        # Hacher le mot de passe
        utilisateur.set_password(validated_data['password'])
        utilisateur.save()
        return utilisateur