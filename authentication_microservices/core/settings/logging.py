import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = "logs"
LOG_DIR_PATH = os.path.join(BASE_DIR, LOG_DIR)
if not os.path.exists(LOG_DIR_PATH):
    os.mkdir(LOG_DIR_PATH)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_handler': {
            'level': 'DEBUG',
            'class': 'error_logging.db_log_handler.DatabaseLogHandler',
            'formatter': 'verbose'
        },
        'apiLogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR_PATH, "api_debug_log.log"),
            'when': 'D',
            'backupCount': 2,
            'formatter': 'verbose',
            'utc': True,
        }

    },
    'loggers': {
        'db': {
            'level': 'DEBUG',
            'handlers': ['db_handler']
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['apiLogfile'],
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['apiLogfile'],
            'propagate': True,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['apiLogfile'],
        #     'propagate': True
        # },
        'gunicorn.access': {
            'level': 'DEBUG',
            'handlers': ['apiLogfile'],
            'propagate': False
        }
    }
}
