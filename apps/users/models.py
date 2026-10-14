from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Profil(models.Model):
    """Modèle représentant le profil d'un utilisateur."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_de_profil = models.ImageField(upload_to='profils/', default='profils/default.jpg')
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = PhoneNumberField(blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        """Retourne le nom complet de l'utilisateur."""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username