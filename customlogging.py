
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
        'moves': {
            'format' : '%(botname)s %(game)s %(movenum)s %(movedir)s %(movereason)s'
        },
    }, # formatters

    'handlers' : {
        'rotatingfile' : {
            'level' : 'NOTSET',
            'class' : 'logging.handlers.RotatingFileHandler',
            'formatter' : 'verbose',
            'filename' : 'logs/log.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter' : 'simple'
        }
    }, # handlers

    'root' : {
        'handlers' : ['rotatingfile','console'],
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
