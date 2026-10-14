from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from ..models import Panier, Commande, DetailCommande
from .serializers import PanierSerializer, CommandeSerializer
from apps.products.models import Parfum

class PanierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer le panier de l'utilisateur.
    """
    serializer_class = PanierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne uniquement le panier de l'utilisateur connecté."""
        return Panier.objects.filter(client=self.request.user)
    
    def perform_create(self, serializer):
        """Ajoute un parfum au panier avec l'utilisateur connecté."""
        serializer.save(client=self.request.user)
    
    @action(detail=False, methods=['post'])
    def vider(self, request):
        """
        Action personnalisée : vide le panier de l'utilisateur.
        URL : /panier/vider/
        """
        self.get_queryset().delete()
        return Response(
            {'status': 'success', 'message': 'Panier vidé avec succès.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def valider(self, request):
        """
        Action personnalisée : transforme le panier en commande.
        URL : /panier/valider/
        """
        panier = self.get_queryset()
        
        if not panier.exists():
            return Response(
                {'status': 'error', 'message': 'Votre panier est vide.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier le stock pour chaque article du panier
        for item in panier:
            if item.parfum.quantite_stock < item.quantite:
                return Response(
                    {'status': 'error', 'message': f"Stock insuffisant pour '{item.parfum.nom}'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        with transaction.atomic():
            # Créer la commande
            total = sum(item.sous_total for item in panier)
            commande = Commande.objects.create(
                client=request.user,
                total=total,
                adresse_livraison=request.data.get('adresse_livraison', 'Adresse non fournie'),
                status='confirmee'
            )
            
            # Créer les détails de la commande et mettre à jour le stock
            for item in panier:
                DetailCommande.objects.create(
                    commande=commande,
                    parfum=item.parfum,
                    quantite=item.quantite,
                    prix_unitaire=item.parfum.prix
                )
                # Réduire le stock
                item.parfum.quantite_stock -= item.quantite
                if item.parfum.quantite_stock == 0:
                    item.parfum.est_disponible = False
                item.parfum.save()
            
            # Vider le panier
            panier.delete()
        
        return Response(
            {
                'status': 'success',
                'message': 'Commande validée avec succès ! 🎉',
                'commande_id': commande.id,
                'total': float(total)
            },
            status=status.HTTP_201_CREATED
        )

class CommandeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour consulter les commandes de l'utilisateur.
    (Lecture seule pour les utilisateurs normaux)
    """
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne uniquement les commandes de l'utilisateur connecté."""
        return Commande.objects.filter(client=self.request.user)
    
    def get_serializer_context(self):
        """Ajoute la requête pour que le sérializer puisse utiliser le client."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context