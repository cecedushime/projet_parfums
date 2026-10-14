from rest_framework import serializers
from ..models import Parfum

from rest_framework import serializers
from ..models import Parfum

class ParfumSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle Parfum.
    Transforme les données Parfum en JSON et vice-versa.
    """
    en_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Parfum
        fields = [
            'id', 
            'nom', 
            'description', 
            'marque',
            'categorie',
            'concentration',
            'prix',
            'quantite_stock',
            'est_disponible',
            'en_stock',
            'notes_tete',
            'notes_coeur',
            'notes_fond',
            'image',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']