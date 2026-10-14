from .base import *  # On importe TOUT ce qui est dans base.py

# ==========================================
# 1. MODE DEBUG (ACTIVÉ EN DÉVELOPPEMENT)
# ==========================================
# DEBUG=True affiche les erreurs détaillées dans le navigateur.
# C'est pratique pour déboguer, mais À NE JAMAIS METTRE EN PRODUCTION.
DEBUG = True

# ==========================================
# 2. HÔTES AUTORISÉS
# ==========================================
# En développement, on autorise localhost et 127.0.0.1 (ta machine)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ==========================================
# 3. CLÉ SECRÈTE DE DJANGO
# ==========================================
# Cette clé est utilisée pour signer les sessions, les cookies, etc.
# En développement, on peut la mettre en dur. En prod, elle viendra de .env
SECRET_KEY = 'django-insecure-2u+(%qnooi0(w6p7ceqr_*%^kby+k4=4oqb*@+fxdcuzj6)+&w'

# ==========================================
# 4. BASE DE DONNÉES (SQLite)
# ==========================================
# SQLite est une base de données légère, parfaite pour le développement.
# Elle est stockée dans un fichier (db.sqlite3) à la racine du projet.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================================
# 5. CLÉ DE SIGNATURE JWT
# ==========================================
# On utilise la même clé secrète pour signer les tokens JWT
# SIMPLE_JWT est déjà défini dans base.py, on surcharge juste la clé
SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

# ==========================================
# 6. PAYPAL (Mode Sandbox - POUR TESTER SANS VRAI PAIEMENT)
# ==========================================
# Les clés ci-dessous sont des clés de TEST fournies par PayPal.
# Elles permettent de simuler des paiements sans débiter de vraie carte.
PAYPAL_SANDBOX = True
PAYPAL_CLIENT_ID = 'AVaJSQz0MveF2Ann4MvSQ2cFamSRqsxrIzGbPAoXAJqdFSuXDUs_XxWypuTDuInyjw9gSC6IVc_15_1C'
PAYPAL_SECRET = 'ENYfmQ9cHZigwub6k4LX66t0stw02sZSPsKrFDEEy-AS7yMn1u6gQroxAPPeAjwlb9L9pDJdfwvikrLo'

# ==========================================
# 7. ENVOI D'EMAILS (Mode console)
# ==========================================
# En développement, les emails sont affichés dans le terminal au lieu d'être envoyés.
# C'est pratique pour tester sans spammer de vraies adresses.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==========================================
# 8. LOGGING (Journalisation)
# ==========================================
# Permet d'afficher les logs dans la console pour déboguer
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # Affiche les messages d'information et plus graves
    },
}

