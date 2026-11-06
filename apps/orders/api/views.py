from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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

class CommandeViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commandes (Création et Lecture).
    """
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne uniquement les commandes de l'utilisateur connecté."""
        return Commande.objects.filter(client=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        """
        Crée une commande à partir du panier envoyé par React.
        Exemple de body JSON : { "panier": [ {"id": 1, "quantite": 2} ] }
        """
        panier_data = request.data.get('panier', [])
        
        if not panier_data:
            return Response(
                {"error": "Le panier est vide."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic(): # Sécurité : si ça plante, tout est annulé
                total = 0
                parfums_a_commander = []
                
                # 1. Vérification des stocks et calcul du total
                for item in panier_data:
                    parfum = Parfum.objects.get(id=item['id'])
                    quantite = item['quantite']
                    
                    if parfum.quantite_stock < quantite:
                        raise ValueError(f"Stock insuffisant pour le parfum : {parfum.nom}")
                    
                    total += parfum.prix * quantite
                    parfums_a_commander.append((parfum, quantite))

                # 2. Création de la commande
                commande = Commande.objects.create(
                    client=request.user,
                    total=total,
                    adresse_livraison="Adresse par défaut", 
                    status='en_attente'
                )

                # 3. Création des détails et mise à jour du stock
                for parfum, quantite in parfums_a_commander:
                    DetailCommande.objects.create(
                        commande=commande,
                        parfum=parfum,
                        quantite=quantite,
                        prix_unitaire=parfum.prix
                    )
                    parfum.quantite_stock -= quantite
                    parfum.save()

            return Response(
                {"message": "Commande créée avec succès !", "commande_id": commande.id},
                status=status.HTTP_201_CREATED
            )

        except Parfum.DoesNotExist:
            return Response({"error": "Un des parfums n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)