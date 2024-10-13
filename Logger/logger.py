import logging, logging.config, os

class Logger:
    '''
    Logger class is responsible for handling the logging actions.
    
    Attributes:
        config (dict): The logger configuration options
        logger (logging.Logger): The logger instance
    '''
    def __init__(self, config_path='Logger/logging.conf', log_dir='logs', logger_name='api_logger'):
        self.config_path = config_path
        self.log_dir = log_dir
        self.logger_name = logger_name
        self.__setup_logger()

    def __setup_logger(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        logging.config.fileConfig(self.config_path)

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.info(f'{self.logger_name} initialized.')
        return logger