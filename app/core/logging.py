# app/core/logging.py
import logging
import logging.config

def setup_logging():
    """Configure the logging for the application."""
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "loggers": {
            # Libraries: quiet
            "":               {"handlers": ["console"], "level": "WARNING"},
            "uvicorn":        {"level": "WARNING", "propagate": False},
            "uvicorn.error":  {"level": "WARNING", "propagate": False},
            "uvicorn.access": {"level": "WARNING", "propagate": False},

            # Your app: show INFO (this is what you'll use via logging.getLogger(__name__))
            "app":            {"handlers": ["console"], "level": "INFO", "propagate": False},
        },
    })
