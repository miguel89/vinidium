
import logging
import logging.config
from pathlib import Path


LOGCONFIG = {
    'version' : 1,
    'disable_existing_loggers' : True,

    'formatters' : {
        'verbose': {
            'format' : '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format' : '%(levelname)s %(message)s'
        },
    }, # formatters

    'handlers' : {
        'rotatingfile' : {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'formatter' : 'verbose',
            'filename' : 'logs/log.log',
        },
        'everything' : {
            'level' : 'NOTSET',
            'class' : 'logging.handlers.RotatingFileHandler',
            'formatter' : 'verbose',
            'filename' : 'logs/everything.log',
        },

        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter' : 'simple'
        }
    }, # handlers

    'root' : {
        'handlers' : ['rotatingfile','console', 'everything'],
        'propagate': True,
        'level': 'NOTSET'
    } # loggers
} # Logconfig


# evidently the best way to write `mkdir -p`???
with Path('logs') as path:
    if not path.exists():
        path.mkdir(parents=True)

logging.config.dictConfig(LOGCONFIG)

logger = logging.getLogger(__name__)

logger.debug("Logging configured.")
