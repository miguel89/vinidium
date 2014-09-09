
import logging
import logging.config

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
            'level' : 'NOTSET',
            'class' : 'logging.handlers.RotatingFileHandler',
            'formatter' : 'verbose',
            'filename' : 'log/log.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        }
    }, # handlers

    'root' : {
        'handlers' : ['rotatingfile','console'],
        'propagate': True,
        'level': 'NOTSET'
    } # loggers
} # Logconfig

logging.config.dictConfig(LOGCONFIG)

logger = logging.getLogger(__name__)

logger.info("Logging configured.")
