from rest_framework import serializers
from ..models import Panier, Commande, DetailCommande
from apps.products.api.serializers import ParfumSerializer

class PanierSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle Panier.
    """
    parfum = ParfumSerializer(read_only=True)
    parfum_id = serializers.PrimaryKeyRelatedField(
        queryset=Parfum.objects.all(),
        source='parfum',
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
            'parfum',
            'parfum_id',
            'quantite',
            'sous_total',
            'date_ajout'
        ]
        read_only_fields = ['date_ajout']

class DetailCommandeSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle DetailCommande.
    """
    parfum = ParfumSerializer(read_only=True)
    sous_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = DetailCommande
        fields = [
            'id',
            'parfum',
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