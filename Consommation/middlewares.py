from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthenticationFromCookies(JWTAuthentication):
    def authenticate(self, request):
        # Vérifie le cookie pour le token d'accès
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                # Valide le token en utilisant la méthode `get_validated_token` et `get_user`
                validated_token = self.get_validated_token(access_token)
                return self.get_user(validated_token), validated_token
            except AuthenticationFailed:
                pass
        return None