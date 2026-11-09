"""
Configuration des URLs principales du projet SmartPC.

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


from apps.products.api.views import ProduitViewSet
from apps.orders.api.views import PanierViewSet, CommandeViewSet

# ==========================================
# CRÉATION DU ROUTEUR PRINCIPAL
# ==========================================
router = DefaultRouter()


router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'panier', PanierViewSet, basename='panier')
router.register(r'commandes', CommandeViewSet, basename='commande')

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ==========================================
    # DOCUMENTATION DE L'API (SWAGGER / OPENAPI)
    # ==========================================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # ==========================================
    # API VERSION 1
    # ==========================================
    path('api/v1/', include(router.urls)),
]

# ==========================================
# FICHIERS MÉDIAS (EN DÉVELOPPEMENT)
# ==========================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)