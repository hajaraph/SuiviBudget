from functools import wraps

from django.db.models import ProtectedError
from django.db.models.functions import ExtractMonth, TruncWeek
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from Consommation.models import Service, Consommable, Stock, Utilisateur
from Consommation.serializers import UserSerializer, ServiceSerializer, ConsommableSerializer, StockSerializer, \
    ConsommationSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, F
from django.db.models.functions import ExtractYear
from datetime import date
from .models import Consommation


def is_admin_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.est_admin:
            raise PermissionDenied("Vous devez être administrateur pour accéder à cette ressource.")
        return func(request, *args, **kwargs)
    return inner


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_annual_cost_totals(request):
    utilisateur = request.user
    year = request.query_params.get('year', date.today().year)

    if utilisateur.est_admin:
        cout_par_annee = (
            Consommation.objects
            .annotate(annee=ExtractYear('date_conso'))
            .filter(annee=year)
            .values('annee')
            .annotate(
                total_cout=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))
            )
        )
    else:
        cout_par_annee = (
            Consommation.objects
            .annotate(annee=ExtractYear('date_conso'))
            .filter(
                annee=year,
                utilisateur__service=utilisateur.service
            )
            .values('annee')
            .annotate(
                total_cout=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))
            )
        )

    # Vérifier si des données existent
    if not cout_par_annee.exists():
        return Response({"message": "Aucune donnée trouvée pour l'année spécifiée."}, status=404)

    return Response(cout_par_annee[0])



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mois_cost_totals(request):
    utilisateur = request.user
    year = request.query_params.get('year', date.today().year)

    if utilisateur.est_admin:
        cout_par_mois = (
            Consommation.objects
            .annotate(annee=ExtractYear('date_conso'), mois=ExtractMonth('date_conso'))  # Extraire année et mois
            .filter(annee=year)  # Filtrer par année donnée
            .values('mois')  # Grouper par mois
            .annotate(
                total_cout=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))
            )
            .order_by('mois')
        )
    else:
        cout_par_mois = (
            Consommation.objects
            .annotate(annee=ExtractYear('date_conso'), mois=ExtractMonth('date_conso'))  # Extraire année et mois
            .filter(
                annee=year,
                utilisateur__service=utilisateur.service,
            )  # Filtrer par année donnée
            .values('mois')  # Grouper par mois
            .annotate(
                total_cout=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))
            )
            .order_by('mois')
        )

    # Formater les résultats pour inclure tous les mois même avec un total de 0
    results = [{"mois": mois, "total_cout": 0} for mois in range(1, 13)]
    for item in cout_par_mois:
        results[item['mois'] - 1]['total_cout'] = item['total_cout']

    return Response({"annee": year, "details_par_mois": results})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weekly_cost_totals(request):
    utilisateur = request.user
    year = request.query_params.get('year', date.today().year)

    if utilisateur.est_admin:
        cout_par_semaine = (
            Consommation.objects
            .annotate(semaine=TruncWeek('date_conso'))  # Regrouper par semaine
            .filter(date_conso__year=year)  # Filtrer par année donnée
            .values('semaine')  # Grouper par semaine
            .annotate(
                total_cout=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))  # Coût total
            )
            .order_by('semaine')  # Trier par semaine
        )
    else:
        cout_par_semaine = (
            Consommation.objects
            .annotate(semaine=TruncWeek('date_conso'))  # Regrouper par semaine
            .filter(
                date_conso__year=year,
                utilisateur__service=utilisateur.service,
            )  # Filtrer par année donnée
            .values('semaine')  # Grouper par semaine
            .annotate(
                total_cout=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))  # Coût total
            )
            .order_by('semaine')  # Trier par semaine
        )

    if not cout_par_semaine.exists():
        return Response({"annee": year, "details_par_semaine": []})

    # Retourner la réponse avec les résultats
    results = [
        {
            'semaine': item['semaine'].strftime('%Y-%m-%d'),
            'total_cout': item['total_cout'],
        }
        for item in cout_par_semaine
    ]

    return Response({"annee": year, "details_par_semaine": results})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_service_consumption_by_year(request):
    utilisateur = request.user
    year = request.query_params.get('year', date.today().year)

    results = []

    if utilisateur.est_admin:
        consumption_per_year = (
            Consommation.objects
            .filter(date_conso__year=year)
            .values('service')
            .annotate(
                total_cost=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))
            )
        )
        all_services = Service.objects.all()

        # Ajouter tous les services avec leur coût total, même ceux sans consommation
        for service in all_services:
            consumption_data = next(
                (item for item in consumption_per_year if item['service'] == service.id_service),
                None
            )

            # Si aucune consommation n'a été trouvée pour ce service, le coût total est 0
            total_cost = consumption_data['total_cost'] if consumption_data else 0

            results.append({
                'annee': year,
                'service': service.nom_service,
                'total_cost': total_cost,
            })

    else:
        consumption_per_year = (
            Consommation.objects
            .filter(
                date_conso__year=year,
                utilisateur__service__id_service=utilisateur.service.id_service
            )
            .values('service')
            .annotate(
                total_cost=Sum(F('quantite_conso') * F('stock__consommable__prix_unitaire'))
            )
        )

        # Ajouter les résultats spécifiques à son service
        if consumption_per_year:
            consumption_data = consumption_per_year[0]
            service = Service.objects.get(id_service=consumption_data['service'])
            results.append({
                'annee': year,
                'service': service.nom_service,
                'total_cost': consumption_data['total_cost'],
            })

    return Response(results)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = get_user_model().objects.get(nom_utilisateur=request.data['nom_utilisateur'])

            # Ajouter les informations supplémentaires de l'utilisateur
            response.data['utilisateur'] = {
                'nom_utilisateur': user.nom_utilisateur,
                'numero_utilisateur': user.numero_utilisateur,
                'est_admin': user.est_admin,
                'service_id': user.service.id_service if user.service else None,
            }

        return response


class Inscrire(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class UtilisateurDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        utilisateurs = Utilisateur.objects.all()

        list_utilisateurs = []
        for utilisateur in utilisateurs:
            donne = {
                'id': utilisateur.pk,
                'nom_utilisateur': utilisateur.nom_utilisateur,
                'numero_utilisateur': utilisateur.numero_utilisateur,
                'est_admin': utilisateur.est_admin,
                'date_joined': utilisateur.date_joined,
                'service': utilisateur.service.nom_service if utilisateur.service else None,
            }
            list_utilisateurs.append(donne)

        return Response(list_utilisateurs)

    @staticmethod
    def put(request, pk=None):
        utilisateur = get_object_or_404(Utilisateur, pk=pk)
        serializer = UserSerializer(utilisateur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk=None):
        utilisateur = get_object_or_404(Utilisateur, pk=pk)
        utilisateur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk=None):
        if pk:
            service = get_object_or_404(Service, pk=pk)
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)

    @staticmethod
    @is_admin_required
    def post(request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @is_admin_required
    def put(request, pk=None):
        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @is_admin_required
    def delete(request, pk=None):
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsommableView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk=None):
        if pk is None:
            consommable = Consommable.objects.all()
            serializer = ConsommableSerializer(consommable, many=True)
            return Response(serializer.data)
        else:
            consommable = get_object_or_404(Consommable, pk=pk)
            serializer = ConsommableSerializer(consommable, many=True)
            return Response(serializer.data)

    @staticmethod
    @is_admin_required
    def post(request):
        serializer = ConsommableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @is_admin_required
    def put(request, pk=None):
        consommable = get_object_or_404(Consommable, pk=pk)
        serializer = ConsommableSerializer(consommable, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @is_admin_required
    def delete(request, pk=None):
        consommable = get_object_or_404(Consommable, pk=pk)
        try:
            consommable.delete()
            return Response(
                {"message": "Consommable supprimé avec succès !"},
                status=status.HTTP_204_NO_CONTENT
            )
        except ProtectedError:
            return Response(
                {"error": "Ce consommable est déjà utilisé dans une autre table et ne peut pas être supprimé."},
                status=status.HTTP_400_BAD_REQUEST
            )


class StockView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk=None):
        if pk:
            stock = get_object_or_404(Stock, pk=pk)
            serializer = StockSerializer(stock)
            return Response(serializer.data)
        else:
            stocks = Stock.objects.all()
            list_stock = [
                {
                    'id_stock': stock.id_stock,
                    'quantite_stock': stock.quantite_stock,
                    'consommables': {
                        'id_consommable': stock.consommable_id,
                        'nom_consommable': stock.consommable.nom_consommable,
                        'categorie': stock.consommable.categorie
                    },
                    'date_maj_stock': stock.date_maj_stock,
                    'utilisateur': {
                        'id': stock.utilisateur_id,
                        'nom_utilisateur': stock.utilisateur.nom_utilisateur,
                        'est_admin': stock.utilisateur.est_admin
                    }
                }
                for stock in stocks
            ]

            return Response(list_stock)

    @staticmethod
    @is_admin_required
    def post(request):
        data = request.data.copy()
        data['utilisateur'] = request.user.id

        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Stock ajouté ou mis à jour avec succès."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @is_admin_required
    def delete(request, pk=None):
        stock = get_object_or_404(Stock, pk=pk)
        stock.delete()
        return Response({"message": "Stock supprimé avec succès !"}, status=status.HTTP_204_NO_CONTENT)


class ConsoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk=None):
        if pk:
            conso = get_object_or_404(Consommation, pk=pk)
            serializer = ConsommationSerializer(conso)
            return Response(serializer.data)

        else:
            consos = Consommation.objects.all()
            serializer = ConsommationSerializer(consos, many=True)
            return Response(serializer.data)

    @staticmethod
    @is_admin_required
    def post(request):
        data = request.data.copy()
        data['utilisateur'] = request.user.id

        serializer = ConsommationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    @is_admin_required
    def delete(request, pk=None):
        conso = get_object_or_404(Consommation, pk=pk)
        conso.delete()
        return Response({'message': 'Consommation supprimer avec succès !'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verification(request):
    utilisateur = request.user

    if utilisateur.est_admin:
        return Response({"est_admin": True})

    return Response({"est_admin": False})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alrt_stock_epuise(request):
    utilisateur = request.user
