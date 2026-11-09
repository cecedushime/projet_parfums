from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..models import ProduitInformatique
from .serializers import ProduitSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import StandardPagination

class ProduitViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les produits informatiques.
    
    Actions disponibles :
    - GET /produits/ : Liste tous les produits
    - POST /produits/ : Crée un nouveau produit (admin uniquement)
    - GET /produits/{id}/ : Détail d'un produit
    - PUT /produits/{id}/ : Modifie un produit (admin uniquement)
    - DELETE /produits/{id}/ : Supprime un produit (admin uniquement)
    - GET /produits/disponibles/ : Liste des produits en stock
    """
    queryset = ProduitInformatique.objects.all()
    serializer_class = ProduitSerializer
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
        'est_disponible'
    ]
    search_fields = [
        'nom',
        'description',
        'marque',
        'processeur',
        'carte_graphique'
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
        Action personnalisée : retourne les produits disponibles.
        URL : /produits/disponibles/
        """
        produits = ProduitInformatique.objects.filter(est_disponible=True, quantite_stock__gt=0)
        serializer = self.get_serializer(produits, many=True)
        return Response({
            'status': 'success',
            'count': produits.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def acheter(self, request, pk=None):
        """
        Action personnalisée : simule l'achat d'un produit.
        URL : /produits/{id}/acheter/
        """
        produit = self.get_object()
        
        # Vérifier le stock
        if produit.quantite_stock <= 0:
            return Response(
                {'status': 'error', 'message': f"Le produit '{produit.nom}' n'est plus en stock."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Réduire le stock (simulation d'achat)
        produit.quantite_stock -= 1
        if produit.quantite_stock == 0:
            produit.est_disponible = False
        produit.save()
        
        return Response({
            'status': 'success',
            'message': f"Vous avez acheté '{produit.nom}' avec succès ! 🎉",
            'produit': {
                'id': produit.id,
                'nom': produit.nom,
                'marque': produit.marque,
                'prix': float(produit.prix),
                'quantite_restante': produit.quantite_stock
            }
        })