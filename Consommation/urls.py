from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from Consommation.views import Inscrire, CustomTokenObtainPairView, ServiceView

urlpatterns = [
    path('connexion', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('inscrire', Inscrire.as_view()),
    path('service', ServiceView.as_view()),
    path('service/update/<int:pk>', ServiceView.as_view()),
    path('service/delete/<int:pk>', ServiceView.as_view()),
]
