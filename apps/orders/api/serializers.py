from rest_framework import serializers
from ..models import Panier, Commande, DetailCommande
from apps.products.api.serializers import ParfumSerializer

class PanierSerializer(serializers.ModelSerializer):
    parfum = ParfumSerializer(read_only=True)
    sous_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Panier
        fields = ['id', 'parfum', 'quantite', 'sous_total', 'date_ajout']

class DetailCommandeSerializer(serializers.ModelSerializer):
    parfum = ParfumSerializer(read_only=True)
    sous_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = DetailCommande
        fields = ['id', 'parfum', 'quantite', 'prix_unitaire', 'sous_total']

class CommandeSerializer(serializers.ModelSerializer):
    details = DetailCommandeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Commande
        fields = ['id', 'client', 'date_commande', 'total', 'status', 'details']