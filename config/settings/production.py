"""
Fichier de configuration pour l'ENVIRONNEMENT DE PRODUCTION - Projet Parfums
Utilisé sur le serveur en ligne.
- DEBUG = False (pas d'affichage des erreurs)
- Base de données PostgreSQL (robuste)
- Toutes les clés viennent du fichier .env (SÉCURITÉ)
- HTTPS activé
"""

import os
from .base import *  # On importe TOUT ce qui est dans base.py

# ==========================================
# 1. MODE DEBUG (DÉSACTIVÉ EN PRODUCTION)
# ==========================================
# DEBUG=False empêche l'affichage des erreurs détaillées aux utilisateurs.
# Les erreurs sont enregistrées dans des logs.
DEBUG = False

# ==========================================
# 2. HÔTES AUTORISÉS (VIENNENT DU FICHIER .env)
# ==========================================
# Exemple : "mondomaine.com,www.mondomaine.com"
# On lit la variable d'environnement ALLOWED_HOSTS et on la découpe en liste.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# ==========================================
# 3. CLÉ SECRÈTE (DOIT VENIR DU FICHIER .env)
# ==========================================
# La clé secrète ne doit JAMAIS être écrite en dur dans le code.
# Elle est stockée dans un fichier .env qui n'est pas dans Git.
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable d'environnement SECRET_KEY n'est pas définie !")

# ==========================================
# 4. BASE DE DONNÉES (PostgreSQL)
# ==========================================
# PostgreSQL est plus robuste que SQLite pour la production.
# Il supporte plusieurs connexions simultanées et est plus performant.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# ==========================================
# 5. CONFIGURATION CORS (Production)
# ==========================================
# En production, on spécifie EXACTEMENT les origines autorisées
CORS_ALLOW_ALL_ORIGINS = False  # Désactivé en production
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')

# ==========================================
# 6. SÉCURITÉ HTTPS
# ==========================================
# Force le passage en HTTPS et sécurise les cookies
SECURE_SSL_REDIRECT = True              # Redirige HTTP vers HTTPS
CSRF_COOKIE_SECURE = True               # Les cookies CSRF sont envoyés uniquement en HTTPS
SESSION_COOKIE_SECURE = True            # Les cookies de session sont envoyés uniquement en HTTPS
SECURE_HSTS_SECONDS = 31536000          # 1 an : indique aux navigateurs d'utiliser HTTPS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True   # Applique HSTS aux sous-domaines
SECURE_HSTS_PRELOAD = True              # Autorise l'ajout de la liste HSTS préchargée
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==========================================
# 7. CLÉ DE SIGNATURE JWT
# ==========================================
# On utilise la même clé secrète pour signer les tokens JWT
SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

# ==========================================
# 8. PAYPAL (Mode LIVE - PAIEMENTS RÉELS)
# ==========================================
# Les clés PayPal en production doivent venir du fichier .env.
# Ce sont les clés qui permettent de faire des vrais paiements.
PAYPAL_SANDBOX = False
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = os.environ.get('PAYPAL_SECRET')

if not PAYPAL_CLIENT_ID or not PAYPAL_SECRET:
    raise ValueError("Les clés PayPal doivent être définies dans .env !")

# ==========================================
# 9. ENVOI D'EMAILS (SMTP)
# ==========================================
# En production, les emails sont envoyés via un serveur SMTP.
# Les paramètres viennent du fichier .env
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# ==========================================
# 10. FICHIERS STATIQUES (collectés)
# ==========================================
# En production, tous les fichiers statiques sont rassemblés dans staticfiles/
# C'est fait par la commande "python manage.py collectstatic"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==========================================
# 11. LOGGING (Journalisation des erreurs)
# ==========================================
# Les erreurs sont écrites dans un fichier de log pour analyse ultérieure.
# Cela permet de savoir ce qui a planté sans afficher les détails aux utilisateurs.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
            'level': 'ERROR',  # Seules les erreurs graves sont enregistrées
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'ERROR',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'CRITICAL',  # Envoie un email aux admins en cas d'erreur critique
            'include_html': True,
        },
    },
    'root': {
        'handlers': ['file', 'console', 'mail_admins'],
        'level': 'ERROR',
    },
}

# ==========================================
# 12. SÉCURITÉ SUPPLÉMENTAIRE
# ==========================================
# Empêche le site d'être affiché dans une iframe (protection clickjacking)
X_FRAME_OPTIONS = 'DENY'

# Empêche le navigateur de deviner le type de contenu
SECURE_CONTENT_TYPE_NOSNIFF = True

# Protection contre le Cross-Site Scripting (XSS)
SECURE_BROWSER_XSS_FILTER = True