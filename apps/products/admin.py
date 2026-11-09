from django.contrib import admin
from .models import ProduitInformatique

@admin.register(ProduitInformatique)
class ProduitAdmin(admin.ModelAdmin):
    # Les colonnes à afficher dans la liste
    list_display = ('nom', 'marque', 'categorie', 'prix', 'quantite_stock', 'est_disponible')
    
    # Les filtres sur le côté droit
    list_filter = ('categorie', 'marque', 'est_disponible')
    
    # La barre de recherche
    search_fields = ('nom', 'marque', 'description', 'processeur', 'carte_graphique')
    
    # L'ordre d'affichage
    ordering = ('-created_at',)