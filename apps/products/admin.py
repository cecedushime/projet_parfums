from django.contrib import admin
from .models import Parfum

@admin.register(Parfum)
class ParfumAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque', 'categorie', 'prix', 'quantite_stock', 'est_disponible')
    list_filter = ('categorie', 'marque', 'est_disponible')
    search_fields = ('nom', 'marque', 'description')
    ordering = ('-created_at',)