from ..settings import *

# add any your code developer add in local settings

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "warning": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/warning/warning.log",
            "level": "WARNING",
            "maxBytes": 1024 * 1024,  # 1 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/debug/debug.log",
            "level": "DEBUG",
            "maxBytes": 1024 * 1024,  # 1 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "query": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/query/django_queries.log",
            "level": "DEBUG",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024,  # 1 MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "warning", "debug"],
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": [
                "query",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
