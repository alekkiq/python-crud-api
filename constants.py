# --------------------------------------------
#
# Define all the constants used in the program.
#
# --------------------------------------------


# ------------------------------ #
# App constants                  #
# ------------------------------ #
from config import app_config as APP_CONFIG

# ------------------------------ #
# Database constants             #
# ------------------------------ #
from config import database_config as DATABASE_CONFIG
    
# ------------------------------ #
# Logger constants               #
# ------------------------------ #

# ------------------------------ #
# API constants                  #
# ------------------------------ #
from config import api_config as API_CONFIG

API_KEYS = set(API_CONFIG().get('keys'))
API_SECRETS = API_CONFIG().get('secrets')
HIDDEN_TABLES = API_CONFIG().get('hidden_tables')
ALLOWED_ORIGINS = API_CONFIG().get('allowed_origins')


# ------------------------------ #
# API Route constants            #
# ------------------------------ #
API_CORE_URL_PREFIX = '/api/v1'
API_REQUEST_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
VALID_GET_QUERY_ARGS = ['where', 'order_by', 'sort', 'limit', 'offset']


# ------------------------------ #
# Other constants                #
# ------------------------------ #
# ...