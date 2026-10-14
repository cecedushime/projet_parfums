"""
Configuration des URLs principales du projet Parfums.

Ce fichier est le point d'entrée de toutes les URLs du projet.
Il redirige vers les différentes applications et endpoints.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from apps.products.api.views import ParfumViewSet
from apps.orders.api.views import PanierViewSet, CommandeViewSet

# ==========================================
# IMPORTS DES VIEWSETS
# ==========================================
# Quand tu auras créé tes vues, tu décommenteras ces imports
# from apps.products.api.views import ParfumViewSet
# from apps.orders.api.views import PanierViewSet, CommandeViewSet
# from apps.users.api.views import UserViewSet, ProfilViewSet

# ==========================================
# CRÉATION DU ROUTEUR PRINCIPAL
# ==========================================
# Le routeur génère automatiquement les URLs pour les ViewSets
router = DefaultRouter()

# Enregistrement des ViewSets (à décommenter quand les vues sont créées)
router.register(r'parfums', ParfumViewSet, basename='parfum')
router.register(r'panier', PanierViewSet, basename='panier')
router.register(r'commandes', CommandeViewSet, basename='commande')
# router.register(r'users', UserViewSet, basename='user')

# ==========================================
# LISTE DES URLs PRINCIPALES
# ==========================================
urlpatterns = [
    # ==========================================
    # ADMIN DJANGO
    # ==========================================
    path('admin/', admin.site.urls),
    
    # ==========================================
    # AUTHENTIFICATION JWT (JSON Web Token)
    # ==========================================
    # Obtenir un token (login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Rafraîchir un token (quand il expire)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Vérifier un token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ==========================================
    # DOCUMENTATION DE L'API (SWAGGER / OPENAPI)
    # ==========================================
    # Schéma OpenAPI (JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Interface Swagger UI (interface interactive)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Interface ReDoc (alternative à Swagger)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # ==========================================
    # API VERSION 1
    # ==========================================
    # Toutes les URLs de l'API v1 (générées par le routeur)
    path('api/v1/', include(router.urls)),
]

# ==========================================
# FICHIERS MÉDIAS (EN DÉVELOPPEMENT)
# ==========================================
# En développement, Django sert les fichiers médias (images uploadées)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)