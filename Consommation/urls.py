from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from Consommation.views import Inscrire, CustomTokenObtainPairView, ServiceView, ConsommableView, StockView, ConsoView, \
    UtilisateurDetail, get_annual_cost_totals, get_mois_cost_totals, get_weekly_cost_totals, \
    get_service_consumption_by_year, verification

urlpatterns = [
    path('connexion', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('inscrire', Inscrire.as_view()),
    path('utilisateur', UtilisateurDetail.as_view()),
    path('utilisateur/update/<int:pk>', UtilisateurDetail.as_view()),
    path('utilisateur/delete/<int:pk>', UtilisateurDetail.as_view()),
    path('service', ServiceView.as_view()),
    path('service/update/<int:pk>', ServiceView.as_view()),
    path('service/delete/<int:pk>', ServiceView.as_view()),
    path('consommable', ConsommableView.as_view()),
    path('consommable/update/<int:pk>', ConsommableView.as_view()),
    path('consommable/delete/<int:pk>', ConsommableView.as_view()),
    path('stock', StockView.as_view()),
    path('stock/delete/<int:pk>', StockView.as_view()),
    path('consommation', ConsoView.as_view()),

    path('consommation/delete/<int:pk>', ConsoView.as_view()),
    path('accueil/annee', get_annual_cost_totals),
    path('accueil/mois', get_mois_cost_totals),

    path('accueil/semaine', get_weekly_cost_totals),
    path('accueil/service', get_service_consumption_by_year),
    path('admin', verification),
]
