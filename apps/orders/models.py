from django.db import models
from django.conf import settings
from apps.products.models import Parfum

class Panier(models.Model):
    """
    Modèle représentant le panier d'un utilisateur.
    Un utilisateur peut avoir plusieurs parfums dans son panier.
    """
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='panier'
    )
    parfum = models.ForeignKey(
        Parfum,
        on_delete=models.CASCADE,
        related_name='panier_items'
    )
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('client', 'parfum')  # Empêche les doublons
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.client.username} - {self.parfum.nom} x{self.quantite}"

    @property
    def sous_total(self):
        """Calcule le sous-total pour cet article du panier."""
        return self.quantite * self.parfum.prix


class Commande(models.Model):
    """
    Modèle représentant une commande finalisée.
    """
    STATUS_CHOICES = [
        ('en_attente', 'En attente de paiement'),
        ('confirmee', 'Confirmée'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    date_commande = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='en_attente'
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="ID de la transaction PayPal ou Stripe"
    )
    adresse_livraison = models.TextField()
    
    # Date de livraison estimée (calculée automatiquement plus tard)
    date_livraison_estimee = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_commande']

    def __str__(self):
        return f"Commande #{self.id} - {self.client.username}"

    @property
    def est_payee(self):
        """Vérifie si la commande a été payée."""
        return self.status not in ['en_attente', 'annulee']


class DetailCommande(models.Model):
    """
    Modèle représentant les détails d'une commande.
    Chaque commande peut avoir plusieurs parfums.
    """
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='details'
    )
    parfum = models.ForeignKey(
        Parfum,
        on_delete=models.CASCADE,
        related_name='details_commandes'
    )
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.commande.id} - {self.parfum.nom} x{self.quantite}"

    @property
    def sous_total(self):
        """Calcule le sous-total pour cette ligne de commande."""
        return self.quantite * self.prix_unitaire