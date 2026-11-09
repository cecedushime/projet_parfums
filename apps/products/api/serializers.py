from rest_framework import serializers
from ..models import ProduitInformatique

class ProduitSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle ProduitInformatique.
    Transforme les données d'un produit high-tech en JSON et vice-versa.
    """
    en_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ProduitInformatique
        fields = [
            'id', 
            'nom', 
            'description', 
            'marque',
            'categorie',
            'processeur',
            'carte_graphique',
            'ram',
            'stockage',
            'prix',
            'quantite_stock',
            'est_disponible',
            'en_stock',
            'image',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']