from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from Consommation.views import Inscrire, CustomTokenObtainPairView

urlpatterns = [
    path('connexion', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('inscrire', Inscrire.as_view())
]
