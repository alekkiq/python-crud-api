# --------------------------------------------- #
#                                               #
# Define all the constants used in the program  #
#                                               #
# --------------------------------------------- # 
import os
    
# ------------------------------ #
# App constants                  #
# ------------------------------ #
APP_ENVS = ('development', 'production')
    
# ------------------------------ #
# Logger constants               #
# ------------------------------ #
from Logger.logger_setup import get_logger

APP_LOGGER          = get_logger(logger_name='app_logger', log_dir='logs/app')
DB_LOGGER           = get_logger(logger_name='db_logger', log_dir='logs/db')
API_LOGGER          = get_logger(logger_name='api_logger', log_dir='logs/api')
WAITRESS_LOGGER     = None

# Initialize the waitress logger if the APP_ENV is not development
if os.getenv('APP_ENV') != 'development' and os.getenv('APP_ENV') in APP_ENVS:
    WAITRESS_LOGGER     = get_logger(logger_name='waitress_logger', log_dir='logs/waitress')

# ------------------------------ #
# Database constants             #
# ------------------------------ #
ALLOWED_DATABASES = ('mysql', 'postgresql', 'mongodb', 'sqlite')

# ------------------------------ #
# API constants                  #
# ------------------------------ #
def initialize_api_constants(config: dict):
    '''
    Initialize the constants from the config files.
    '''
    global API_KEYS, API_SECRETS, HIDDEN_TABLES, ALLOWED_ORIGINS
    
    API_KEYS            = set(config.get('keys'))
    API_SECRETS         = config.get('secrets')
    HIDDEN_TABLES       = config.get('hidden_tables')
    ALLOWED_ORIGINS     = config.get('allowed_origins')

# ------------------------------ #
# API Route constants            #
# ------------------------------ #
API_CORE_URL_PREFIX     = '/api/v1'
API_REQUEST_METHODS     = ('GET', 'POST', 'PUT', 'DELETE')
VALID_QUERY_ARGS        = {
                            'GET':      ('where', 'order_by', 'sort', 'limit', 'offset'),
                            'POST':     ('data',),
                            'PUT':      ('data', 'where'),
                            'DELETE':   ('where',)
                        }