from rest_framework import serializers
from ..models import Panier, Commande, DetailCommande
from apps.products.api.serializers import ProduitSerializer 
from apps.products.models import ProduitInformatique 

class PanierSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle Panier.
    """
    produit = ProduitSerializer(read_only=True) 
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=ProduitInformatique.objects.all(), 
        source='produit', 
        write_only=True
    )
    sous_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Panier
        fields = [
            'id',
            'produit', 
            'produit_id', 
            'quantite',
            'sous_total',
            'date_ajout'
        ]
        read_only_fields = ['date_ajout']

class DetailCommandeSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle DetailCommande.
    """
    produit = ProduitSerializer(read_only=True) 
    sous_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = DetailCommande
        fields = [
            'id',
            'produit', 
            'quantite',
            'prix_unitaire',
            'sous_total'
        ]

class CommandeSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle Commande.
    """
    details = DetailCommandeSerializer(many=True, read_only=True)
    client = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Commande
        fields = [
            'id',
            'client',
            'date_commande',
            'total',
            'status',
            'transaction_id',
            'adresse_livraison',
            'date_livraison_estimee',
            'details',
            'est_payee'
        ]
        read_only_fields = ['date_commande', 'est_payee']