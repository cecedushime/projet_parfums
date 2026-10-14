from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Parfum
from .serializers import ParfumSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import StandardPagination

class ParfumViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les parfums.
    
    Actions disponibles :
    - GET /parfums/ : Liste tous les parfums
    - POST /parfums/ : Crée un nouveau parfum (admin uniquement)
    - GET /parfums/{id}/ : Détail d'un parfum
    - PUT /parfums/{id}/ : Modifie un parfum (admin uniquement)
    - DELETE /parfums/{id}/ : Supprime un parfum (admin uniquement)
    - GET /parfums/disponibles/ : Liste des parfums en stock
    """
    queryset = Parfum.objects.all()
    serializer_class = ParfumSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'categorie',
        'marque',
        'concentration',
        'est_disponible'
    ]
    search_fields = [
        'nom',
        'description',
        'marque',
        'notes_tete',
        'notes_coeur',
        'notes_fond'
    ]
    ordering_fields = [
        'prix',
        'nom',
        'marque',
        'created_at'
    ]
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Assigner automatiquement le créateur."""
        serializer.save(createur=self.request.user)
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Action personnalisée : retourne les parfums disponibles.
        URL : /parfums/disponibles/
        """
        parfums = Parfum.objects.filter(est_disponible=True, quantite_stock__gt=0)
        serializer = self.get_serializer(parfums, many=True)
        return Response({
            'status': 'success',
            'count': parfums.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def acheter(self, request, pk=None):
        """
        Action personnalisée : simule l'achat d'un parfum.
        URL : /parfums/{id}/acheter/
        """
        parfum = self.get_object()
        
        # Vérifier le stock
        if parfum.quantite_stock <= 0:
            return Response(
                {'status': 'error', 'message': f"Le parfum '{parfum.nom}' n'est plus en stock."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Réduire le stock (simulation d'achat)
        parfum.quantite_stock -= 1
        if parfum.quantite_stock == 0:
            parfum.est_disponible = False
        parfum.save()
        
        return Response({
            'status': 'success',
            'message': f"Vous avez acheté '{parfum.nom}' avec succès ! 🎉",
            'parfum': {
                'id': parfum.id,
                'nom': parfum.nom,
                'marque': parfum.marque,
                'prix': float(parfum.prix),
                'quantite_restante': parfum.quantite_stock
            }
        })