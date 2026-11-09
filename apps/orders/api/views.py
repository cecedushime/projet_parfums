from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction

from ..models import Panier, Commande, DetailCommande
from .serializers import PanierSerializer, CommandeSerializer
from apps.products.models import ProduitInformatique # 👈 Changement ici

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
        """Ajoute un produit au panier avec l'utilisateur connecté."""
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
            if item.produit.quantite_stock < item.quantite: # 👈 Changement ici
                return Response(
                    {'status': 'error', 'message': f"Stock insuffisant pour '{item.produit.nom}'."}, # 👈 Changement ici
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
                    produit=item.produit, # 👈 Changement ici
                    quantite=item.quantite,
                    prix_unitaire=item.produit.prix # 👈 Changement ici
                )
                # Réduire le stock
                item.produit.quantite_stock -= item.quantite # 👈 Changement ici
                if item.produit.quantite_stock == 0:
                    item.produit.est_disponible = False # 👈 Changement ici
                item.produit.save() # 👈 Changement ici
            
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
                produits_a_commander = [] 
                
                # 1. Vérification des stocks et calcul du total
                for item in panier_data:
                    produit = ProduitInformatique.objects.get(id=item['id']) 
                    quantite = item['quantite']
                    
                    if produit.quantite_stock < quantite:
                        raise ValueError(f"Stock insuffisant pour le produit : {produit.nom}") 
                    
                    total += produit.prix * quantite 
                    produits_a_commander.append((produit, quantite)) 

                # 2. Création de la commande
                commande = Commande.objects.create(
                    client=request.user,
                    total=total,
                    adresse_livraison="Adresse par défaut", 
                    status='en_attente'
                )

                # 3. Création des détails et mise à jour du stock
                for produit, quantite in produits_a_commander: 
                    DetailCommande.objects.create(
                        commande=commande,
                        produit=produit, 
                        quantite=quantite,
                        prix_unitaire=produit.prix 
                    )
                    produit.quantite_stock -= quantite 
                    produit.save() 

            return Response(
                {"message": "Commande créée avec succès !", "commande_id": commande.id},
                status=status.HTTP_201_CREATED
            )

        except ProduitInformatique.DoesNotExist: 
            return Response({"error": "Un des produits n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)