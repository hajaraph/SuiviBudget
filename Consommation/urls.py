from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from Consommation.views import Inscrire, CustomTokenObtainPairView, ServiceView, ConsommableView

urlpatterns = [
    path('connexion', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('inscrire', Inscrire.as_view()),
    path('service', ServiceView.as_view()),
    path('service/update/<int:pk>', ServiceView.as_view()),
    path('service/delete/<int:pk>', ServiceView.as_view()),
    path('consommable', ConsommableView.as_view()),
    path('consommable/update/<int:pk>', ConsommableView.as_view()),
    path('consommable/delete/<int:pk>', ConsommableView.as_view()),
]
