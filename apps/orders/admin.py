from django.contrib import admin
from .models import Panier, Commande, DetailCommande

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('client', 'parfum', 'quantite', 'date_ajout')
    list_filter = ('date_ajout',)
    search_fields = ('client__username', 'parfum__nom')

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'total', 'status', 'date_commande')
    list_filter = ('status', 'date_commande')
    search_fields = ('client__username', 'transaction_id')

@admin.register(DetailCommande)
class DetailCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'parfum', 'quantite', 'prix_unitaire')