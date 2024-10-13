# --------------------------------------------
#
# Define all the constants used in the program.
#
# --------------------------------------------
    
# ------------------------------ #
# Logger constants               #
# ------------------------------ #
from logger_setup import get_logger as get_logger

# Initialize the logger instance
LOGGER = get_logger()

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
    
    API_KEYS = set(config.get('keys'))
    API_SECRETS = config.get('secrets')
    HIDDEN_TABLES = config.get('hidden_tables')
    ALLOWED_ORIGINS = config.get('allowed_origins')

# ------------------------------ #
# API Route constants            #
# ------------------------------ #
API_CORE_URL_PREFIX = '/api/v1'
API_REQUEST_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
VALID_QUERY_ARGS = {
    'GET': ['where', 'order_by', 'sort', 'limit', 'offset'],
    'POST': ['data'],
    'PUT': ['data', 'where'],
    'DELETE': ['where']
}