from datetime import timedelta
from pathlib import Path

# Répertoire de base
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète Django
SECRET_KEY = "django-insecure-9r2b_yjnit&jdd0#f^bphrd47w7+z$w)lbmzf*$7&%k+y!h03u"

# Mode debug activé (désactivez en production !)
DEBUG = True

# Hôtes autorisés
ALLOWED_HOSTS = []

# Applications installées
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Consommation",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",  # Ajout pour la gestion des requêtes CORS
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Doit être placé avant CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLs
ROOT_URLCONF = "Consom.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = "Consom.wsgi.application"

# Base de données (SQLite par défaut)
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'conso.sqlite3',
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalisation
LANGUAGE_CODE = "fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Fichiers statiques
STATIC_URL = "static/"

# Clé auto par défaut
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'Consommation.Utilisateur'

# Gestion des sessions et cookies
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# SimpleJWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    # Ajout des paramètres pour cookies (adaptés au mode local)
    'AUTH_COOKIE': 'access_token',  # Nom du cookie pour le token d'accès
    'AUTH_COOKIE_SECURE': False,    # Désactiver en local, activer en production
    'AUTH_COOKIE_HTTPONLY': True,   # Le cookie ne sera pas accessible via JavaScript
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Empêche les envois cross-site sauf navigation

    'REFRESH_COOKIE': 'refresh_token',
    'REFRESH_COOKIE_PATH': '/api/token/refresh/',
    'REFRESH_COOKIE_SECURE': False,
    'REFRESH_COOKIE_HTTPONLY': True,
    'REFRESH_COOKIE_SAMESITE': 'Lax',
}

# Gestion CORS (autorisation des requêtes frontend)
CORS_ALLOW_CREDENTIALS = True  # Nécessaire pour autoriser les cookies
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend en mode développement
]
