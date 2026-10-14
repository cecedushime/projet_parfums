"""
Fichier contenant les permissions personnalisées pour l'API Parfums.

Les permissions sont comme des "videurs" qui vérifient qui peut faire quoi :
- Est-ce que l'utilisateur est connecté ?
- Est-ce qu'il est admin ?
- Est-ce qu'il est le propriétaire de l'objet ?
"""

from rest_framework import permissions

# ==========================================
# 1. PERMISSION : ADMIN OU LECTURE SEULE
# ==========================================
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission : 
    - Les admins peuvent TOUT faire (GET, POST, PUT, DELETE)
    - Les autres utilisateurs peuvent seulement LIRE (GET, HEAD, OPTIONS)
    
    Utilisation typique : pour les parfums (tout le monde peut voir,
    mais seul l'admin peut créer/modifier/supprimer)
    """
    
    def has_permission(self, request, view):
        # Si la méthode est une lecture sécurisée (GET, HEAD, OPTIONS)
        # on autorise tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Sinon (POST, PUT, DELETE), on vérifie que l'utilisateur
        # est connecté ET qu'il est admin (is_staff)
        return request.user.is_authenticated and request.user.is_staff


# ==========================================
# 2. PERMISSION : PROPRIÉTAIRE OU LECTURE SEULE
# ==========================================
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission :
    - Le propriétaire de l'objet peut le modifier ou le supprimer
    - Les autres utilisateurs peuvent seulement LIRE (GET, HEAD, OPTIONS)
    
    Utilisation typique : pour le panier (seul le propriétaire du panier
    peut ajouter/retirer des articles)
    """
    
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS sont autorisés pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Pour les autres méthodes, on vérifie que l'utilisateur
        # connecté est le propriétaire de l'objet.
        # On suppose que l'objet (panier) a un champ 'client' 
        # qui fait référence à l'utilisateur.
        return obj.client == request.user


# ==========================================
# 3. PERMISSION : ADMIN UNIQUEMENT
# ==========================================
class IsAdminUser(permissions.BasePermission):
    """
    Permission :
    - Seuls les admins (is_staff=True) peuvent accéder à la vue.
    
    Utilisation typique : pour les endpoints sensibles
    (ex: statistiques, gestion des utilisateurs)
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


# ==========================================
# 4. PERMISSION : UTILISATEUR CONNECTÉ UNIQUEMENT
# ==========================================
class IsAuthenticatedOrCreate(permissions.BasePermission):
    """
    Permission :
    - Les utilisateurs connectés peuvent tout faire
    - Les utilisateurs non connectés peuvent seulement créer un compte
    
    Utilisation typique : pour l'inscription (les visiteurs peuvent
    s'inscrire, mais doivent être connectés pour le reste)
    """
    
    def has_permission(self, request, view):
        # Si l'utilisateur est connecté, on autorise
        if request.user.is_authenticated:
            return True
        
        # Si l'utilisateur n'est pas connecté, on autorise uniquement
        # la méthode POST (création d'un compte)
        return request.method == 'POST'


# ==========================================
# 5. PERMISSION : COMMANDE DU CLIENT
# ==========================================
class IsCommandeOwner(permissions.BasePermission):
    """
    Permission :
    - Seul le client qui a passé la commande peut la voir
    
    Utilisation typique : pour les commandes (un utilisateur ne peut
    voir que ses propres commandes)
    """
    
    def has_object_permission(self, request, view, obj):
        # L'objet 'Commande' a un champ 'client' qui fait référence
        # à l'utilisateur qui a passé la commande
        return obj.client == request.user