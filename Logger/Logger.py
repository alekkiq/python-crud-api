import logging
import logging.config
import os

class Logger:
    '''
    Logger class is responsible for handling the logging actions.
    
    Attributes:
        logger_name (str): The name of the logger
        log_dir (str): The directory where log files will be stored
        initiated (bool): Flag to indicate if the logger has been initiated
    '''
    _instances = {}
    _initialized_loggers = set()

    def __new__(cls, *args, **kwargs):
        logger_name = kwargs.get('logger_name', 'api_logger')
        if logger_name not in cls._instances:
            instance = super(Logger, cls).__new__(cls)
            instance.initiated = False  # Initialize the attribute here
            cls._instances[logger_name] = instance
        return cls._instances[logger_name]

    def __init__(self, log_dir='logs', logger_name='api_logger'):
        if not self.initiated:
            self.log_dir = log_dir
            self.logger_name = logger_name
            self.__setup_logger()

    def __setup_logger(self):
        # Ensure the base log directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Define the log file path
        log_file = os.path.join(self.log_dir, f'{self.logger_name}.log')
        
        # Ensure the specific log directory exists
        specific_log_dir = os.path.dirname(log_file)
        if not os.path.exists(specific_log_dir):
            os.makedirs(specific_log_dir)

        # Define the logging configuration
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'default',
                    'stream': 'ext://sys.stdout',
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'default',
                    'filename': log_file,
                    'mode': 'a',
                    'maxBytes': 5*1024*1024,
                    'backupCount': 2,
                },
            },
            'loggers': {
                self.logger_name: {
                    'level': 'DEBUG',
                    'handlers': ['console', 'file'],
                    'propagate': False,
                },
            },
        }

        # Apply the logging configuration
        logging.config.dictConfig(logging_config)

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        if self.logger_name not in Logger._initialized_loggers:
            logger.info(f'{self.logger_name.upper()} successfully initialized.')
            Logger._initialized_loggers.add(self.logger_name)
        return logger
    
def create_logger(logger_name='api_logger', log_dir='logs'):
    logger_instance = Logger(log_dir=log_dir, logger_name=logger_name)
    return logger_instance.get_logger()