from django.contrib import admin
from .models import Panier, Commande, DetailCommande

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('client', 'produit', 'quantite', 'date_ajout')
    list_filter = ('date_ajout',)
    search_fields = ('client__username', 'produit__nom') 

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'total', 'status', 'date_commande')
    list_filter = ('status', 'date_commande')
    search_fields = ('client__username', 'transaction_id')

@admin.register(DetailCommande)
class DetailCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'prix_unitaire')