from Logger.Logger import Logger

# Getter function for the logger instance
def get_logger(logger_name='api_logger', config_path='Logger/logging.conf', log_dir='logs'):
    return Logger(config_path=config_path, log_dir=log_dir, logger_name=logger_name).get_logger()