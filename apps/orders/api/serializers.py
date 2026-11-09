from rest_framework import serializers
from ..models import Panier, Commande, DetailCommande
from apps.products.api.serializers import ProduitSerializer

class PanierSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    sous_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Panier
        fields = ['id', 'produit', 'quantite', 'sous_total', 'date_ajout']

class DetailCommandeSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    sous_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = DetailCommande
        fields = ['id', 'produit', 'quantite', 'prix_unitaire', 'sous_total']

class CommandeSerializer(serializers.ModelSerializer):
    details = DetailCommandeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Commande
        fields = ['id', 'client', 'date_commande', 'total', 'status', 'details']