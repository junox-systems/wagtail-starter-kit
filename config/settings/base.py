import os
import re
from pathlib import Path
import environ
# import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    # set casting, default value
    DJANGO_DEBUG=(bool, False),
    ENVIRONMENT=(str, "development"),
    SECRET_KEY=(str, "django-insecure-dummy-key-for-builds-and-dev-only"),
    # DATABASE_URL=(str, "sqlite:///dummy.db"),
    DATABASE_PATH=(str, BASE_DIR / "db/database.db"),
    ALLOWED_HOSTS=(str, "*"),
    CSRF_TRUSTED_ORIGINS=(str, "https://*, http://*"),
    USE_X_FORWARDED_HOST=(bool, False),
    USE_X_FORWARDED_PORT=(bool, False),
    WAGTAIL_SITE_NAME=(str, "Wagtail Starter Kit"),
    WAGTAILADMIN_BASE_URL=(str, "http://localhost:8000"),
)

# Create a directory for SQLite database if it doesn't exist
(BASE_DIR / "db").mkdir(parents=True, exist_ok=True)

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    # "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # Optional Wagtail apps
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    # "wagtail.contrib.search_promotions",
    # Third-party apps
    "taggit",
    "modelcluster",
    # SEO
    "wagtailseo",
    # Caching
    "wagtailcache",
    # Forms
    "wagtail_flexible_forms",
    # Frontend integration
    "django_vite",
    "turbo_helper",
    # Our apps
    "apps.core",
    "apps.pages",
    "apps.blocks",
    "apps.navigation.apps.NavigationConfig",
    "apps.settings",
    "apps.search",
    "apps.forms",
    "apps.snippets",
]

MIDDLEWARE = [
    "wagtailcache.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "turbo_helper.middleware.TurboMiddleware",
    "wagtailcache.cache.FetchFromCacheMiddleware",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     "default": dj_database_url.config(
#         default=env("DATABASE_URL"),
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": env("DATABASE_PATH"),
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size=134217728;
                PRAGMA journal_size_limit=27103364;
                PRAGMA cache_size=2000;
                PRAGMA busy_timeout=5000;
            """,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Ensure the directory exists to prevent django staticfiles.W004 warning
(BASE_DIR / "frontend/dist").mkdir(parents=True, exist_ok=True)

STATICFILES_DIRS = [
    BASE_DIR / "frontend/dist",  # Vite build output
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

# S3 settings for media files (used by default)
STORAGES = {
    "default": {
        "BACKEND": "config.storage.CustomS3Boto3Storage",
        "OPTIONS": {
            "public_endpoint_url": env(
                "AWS_S3_PUBLIC_ENDPOINT_URL", default="http://localhost:9000"
            ),
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Increase the maximum number of fields for complex page models
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Webpack loader settings
WEBPACK_LOADER = {
    "MANIFEST_FILE": os.path.join(BASE_DIR, "apps/frontend/build/manifest.json"),
}
