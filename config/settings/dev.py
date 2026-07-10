import os
import re

from .base import *  # noqa: F401, F403
from .base import env, MIDDLEWARE, environ, BASE_DIR, STORAGES

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# WhiteNoise for serving static files in development
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")


# http://whitenoise.evans.io/en/stable/django.html#WHITENOISE_IMMUTABLE_FILE_TEST
def immutable_file_test(path, url):
    # Match vite (rollup)-generated hashes, à la, `some_file-CSliV9zW.js`
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test

# Django-Vite Settings
# ------------------------------------------------------------------------------
DJANGO_VITE = {
    "default": {
        "dev_mode": True,
        "dev_server_host": "localhost",
        "dev_server_port": 5173,
    }
}

# Disable wagtail cache in development
WAGTAIL_CACHE = False

DEBUG = True
SECRET_KEY = env("SECRET_KEY")

# Wagtail settings
WAGTAIL_SITE_NAME = "Wagtail Starter Kit"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="minioadmin")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="minioadmin")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="bucket")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default=None)
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = True

# When using MinIO, we need to set this to False to avoid SSL issues
AWS_S3_SECURE_URLS = env("AWS_S3_SECURE_URLS", default=True)

# Ensure query string authentication is enabled and set expiration
AWS_QUERYSTRING_EXPIRE = env(
    "AWS_QUERYSTRING_EXPIRE", default=1800
)  # 1/2 hour expiration

# SECURITY WARNING: define the correct hosts in production!
# This should be set to your domain or IP address in production
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST")
USE_X_FORWARDED_PORT = env("USE_X_FORWARDED_PORT")

STORAGES["default"]["OPTIONS"]["public_endpoint_url"] = env(
    "AWS_S3_PUBLIC_ENDPOINT_URL", default="http://localhost:9000"
)
