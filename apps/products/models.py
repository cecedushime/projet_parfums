from django.db import models
from django.conf import settings

class Parfum(models.Model):
    """
    Modèle représentant un parfum dans la boutique.
    """
    CATEGORIE_CHOICES = [
        ('femme', 'Femme'),
        ('homme', 'Homme'),
        ('unisexe', 'Unisexe'),
    ]
    
    CONCENTRATION_CHOICES = [
        ('eau_de_parfum', 'Eau de Parfum (EDP)'),
        ('eau_de_toilette', 'Eau de Toilette (EDT)'),
        ('eau_de_cologne', 'Eau de Cologne'),
        ('extrait', 'Extrait de Parfum'),
    ]
    
    # Informations principales
    nom = models.CharField(max_length=200)
    description = models.TextField()
    marque = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    concentration = models.CharField(
        max_length=20,
        choices=CONCENTRATION_CHOICES,
        default='eau_de_parfum'
    )
    
    # Prix et stock
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField(default=0)
    est_disponible = models.BooleanField(default=True)
    
    # Notes olfactives (séparées par des virgules)
    notes_tete = models.CharField(max_length=200, blank=True, help_text="Notes de tête (ex: bergamote, citron)")
    notes_coeur = models.CharField(max_length=200, blank=True, help_text="Notes de cœur (ex: jasmin, rose)")
    notes_fond = models.CharField(max_length=200, blank=True, help_text="Notes de fond (ex: vanille, musc)")
    
    # Image
    image = models.ImageField(upload_to='parfums/', null=True, blank=True)
    
    # Métadonnées
    createur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parfums_crees'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['marque']),
            models.Index(fields=['categorie']),
        ]

    def __str__(self):
        return f"{self.nom} - {self.marque}"

    @property
    def en_stock(self):
        """Vérifie si le parfum est en stock."""
        return self.quantite_stock > 0

    @property
    def est_en_promotion(self):
        """Propriété pour les futures promotions (placeholder)."""
        return False