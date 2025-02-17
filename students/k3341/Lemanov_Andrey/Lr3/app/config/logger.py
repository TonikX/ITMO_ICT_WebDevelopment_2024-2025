import logging.config
from students.k3341.Lemanov_Andrey.Lr3.app.config.config import config
import urllib3

urllib3.disable_warnings()


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthz") == -1


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': config.logger.CONSOLE_LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'cmdstanpy': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'prophet': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'uvicorn': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
