import logging, logging.config, os

# Create the log directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')
    
# Load the logging configuration
logging.config.fileConfig('Logger/logging.conf')

# Create the logger
logger = logging.getLogger('simpleExample')