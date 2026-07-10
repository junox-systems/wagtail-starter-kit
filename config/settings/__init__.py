import os

_settings = os.environ.get("DJANGO_SETTINGS_MODULE", "")

if _settings == "config.settings.prod":
    from .prod import *  # noqa: F401, F403
else:
    from .dev import *  # noqa: F401, F403
