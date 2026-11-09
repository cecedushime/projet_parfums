from django.db import models
from django.conf import settings

class ProduitInformatique(models.Model):
    CATEGORIE_CHOICES = [
        ('ordinateur', 'Ordinateur Portable / Bureau'),
        ('composant', 'Composant (Carte graphique, RAM...)'),
        ('accessoire', 'Accessoire (Souris, Clavier...)'),
    ]
    
    nom = models.CharField(max_length=200)
    description = models.TextField()
    marque = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    
    # Les champs spécifiques à l'informatique
    processeur = models.CharField(max_length=100, blank=True)
    ram = models.CharField(max_length=50, blank=True)
    stockage = models.CharField(max_length=50, blank=True)
    carte_graphique = models.CharField(max_length=100, blank=True)
    
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)
    
    
    est_disponible = models.BooleanField(default=True)
    
    createur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produits_crees'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Produit Informatique"
        verbose_name_plural = "Produits Informatiques"

    def __str__(self):
        return f"{self.nom} - {self.marque}"
        
    @property
    def en_stock(self):
        return self.quantite_stock > 0