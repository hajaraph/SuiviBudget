from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from Consommation.models import Service, Consommable, Stock
from Consommation.serializers import UserSerializer, ServiceSerializer, ConsommableSerializer, StockSerializer


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


class ServiceView(APIView):
    permission_classes = [AllowAny]

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
    def post(request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk=None):
        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk=None):
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsommableView(APIView):
    permission_classes = [AllowAny]

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
    def post(request):
        serializer = ConsommableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk=None):
        consommable = get_object_or_404(Consommable, pk=pk)
        serializer = ConsommableSerializer(consommable, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk=None):
        consommable = get_object_or_404(Consommable, pk=pk)
        consommable.delete()
        return Response({"message": "Supprimer avec succès !"}, status=status.HTTP_204_NO_CONTENT)


class StockView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, pk=None):
        if pk:
            stock = get_object_or_404(Stock, pk=pk)
            serializer = StockSerializer(stock)
            return Response(serializer.data)
        else:
            stocks = Stock.objects.all()
            serializer = StockSerializer(stocks, many=True)
            return Response(serializer.data)


    @staticmethod
    def post(request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Stock ajouté ou mis à jour avec succès."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk=None):
        stock = get_object_or_404(Stock, pk=pk)
        stock.delete()
        return Response({"message": "Stock supprimé avec succès !"}, status=status.HTTP_204_NO_CONTENT)
