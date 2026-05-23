"""
Django settings for company project.
"""

from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


# Security (override SECRET_KEY / hosts in production via environment)
DEBUG = env_bool("DJANGO_DEBUG", True)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-%2^1ry32x9sf@ars88lifh7qm+=jlbk(thul57+38!+mg4y%bw"
    else:
        raise ImproperlyConfigured("SECRET_KEY environment variable is required when DJANGO_DEBUG=False.")
_raw_allowed = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _raw_allowed.split(",") if h.strip()]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not DEBUG)
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", 31536000 if not DEBUG else 0))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", not DEBUG)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", not DEBUG)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Installed apps
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
]

if os.environ.get("AWS_STORAGE_BUCKET_NAME"):
    INSTALLED_APPS.append("storages")

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "company.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "company.wsgi.application"

# Database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=int(os.environ.get("DB_CONN_MAX_AGE", "60")),
            ssl_require=env_bool("DATABASE_SSL_REQUIRE", not DEBUG),
        )
    }
elif os.environ.get("DB_HOST"):
    try:
        import pymysql

        pymysql.install_as_MySQLdb()
    except ImportError as exc:
        raise ImproperlyConfigured(
            "PyMySQL is required when DB_HOST is set. Install dependencies from requirements.txt."
        ) from exc

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ.get("DB_PORT", "3306"),
            "NAME": os.environ.get("DB_NAME", ""),
            "USER": os.environ.get("DB_USERNAME") or os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Language & Time
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (optional project-level static dir plus app static assets)
STATIC_URL = "/static/"
_global_static_dir = BASE_DIR / "static"
STATICFILES_DIRS = [_global_static_dir] if _global_static_dir.exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (Images)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

if os.environ.get("AWS_STORAGE_BUCKET_NAME"):
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
    AWS_QUERYSTRING_AUTH = env_bool("AWS_QUERYSTRING_AUTH", False)
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    MEDIA_URL = os.environ.get(
        "MEDIA_URL",
        f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/",
    )
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = (os.environ.get("EMAIL_HOST_USER") or "").strip()
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = (
    (os.environ.get("DEFAULT_FROM_EMAIL") or "").strip()
    or EMAIL_HOST_USER
    or "webmaster@localhost"
)
# Contact form notifications (set CONTACT_EMAIL env, or it defaults to EMAIL_HOST_USER)
CONTACT_EMAIL = (os.environ.get("CONTACT_EMAIL") or "").strip() or EMAIL_HOST_USER

# Auth Redirects
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "Company Admin",
    "site_header": "Company Dashboard",
    "site_brand": "My Company",
    "welcome_sign": "Welcome to Admin Panel",
}

_raw_csrf_origins = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "http://127.0.0.1,http://localhost")
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in _raw_csrf_origins.split(",") if origin.strip()]
