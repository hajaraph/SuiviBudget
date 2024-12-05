from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from Consommation.serializers import UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        user = get_user_model().objects.get(nom_utilisateur=request.data['nom_utilisateur'])

        response.data['utilisateur'] = {
            'nom_utilisateur': user.nom_utilisateur,
            'numero_utilisateur': user.numero_utilisateur,
            'est_admin': user.est_admin,
            'service_id': user.service.id if user.service else None,
        }

        return response


class Inscrire(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
