# ------------------------------------- #
#                                       #
# Main file for running the API.        #
#                                       #
# ------------------------------------ -#

# Python dependencies & external libraries
from flask import Flask, request, jsonify, g, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

# ------------------------------------- #
# Constants & configurations            #
# ------------------------------------- #

# Configurations
from config import DATABASE_CONFIG, API_CONFIG, APP_CONFIG, WAITRESS_CONFIG
from constants import APP_ENVS, API_CORE_URL_PREFIX, API_REQUEST_METHODS, API_ACTION_METHODS, API_DATA_METHODS, API_VALID_CONTENT_TYPES, initialize_api_constants

# Initialize API constants
initialize_api_constants(API_CONFIG)
from constants import API_KEYS, API_SECRETS, API_ALLOWED_ORIGINS, API_PROTECTED_TABLES

# Logger
from constants import APP_LOGGER, DB_LOGGER, API_LOGGER, WAITRESS_LOGGER

# Database modules
from Database import DatabaseFactory, DatabaseManager

# Routes
from Routes.routes import Get as GetRoute, Post as PostRoute, Put as PutRoute, Delete as DeleteRoute

# API status messages
from status import API_STATUS_MESSAGES

# Create the Database instance and the DatabaseManager
database = DatabaseFactory.create_database(DATABASE_CONFIG, DB_LOGGER)
db = DatabaseManager(database, DB_LOGGER)

# Initialize the Flask app
app = Flask(APP_CONFIG.get('name', __name__))

# Enable CORS
CORS(
    app = app, 
    resources = {
        f'{API_CORE_URL_PREFIX}/*': {
                'origins': API_ALLOWED_ORIGINS,
                'methods': list(API_REQUEST_METHODS)
            }
        }, 
    supports_credentials = True
)

# Initialize API limiter
limiter = Limiter(
    app = app,
    key_func = get_remote_address,
    storage_uri = API_CONFIG.get('storage_uri', 'memory://'),
    default_limits = [
        f'{API_CONFIG["limits"]["per_minute"]}/minute',
        f'{API_CONFIG["limits"]["per_hour"]}/hour',
        f'{API_CONFIG["limits"]["per_day"]}/day'
    ]
)

# ------------------------------------- #
# Helper functions                      #
# ------------------------------------- #
def json_result(success: bool, status_message: dict):
    response = {
        'success': success,
        'status': status_message
    }
    return jsonify(response), status_message['code']

# ------------------------------------- #
# Middleware (before_request)           #
# ------------------------------------- #
@app.before_request
def check_api_key():
    '''
    Checks the request headers for the API key and secret.
    '''
    api_key = request.headers.get('X-API-KEY')
    api_secret = request.headers.get('X-API-SECRET')
    
    if api_key not in API_KEYS or API_SECRETS.get(api_key) != api_secret:
        abort(403)  # Forbidden request

@app.before_request
def check_allowed_origin():
    try:
        origin = request.environ.get('HTTP_ORIGIN') or request.environ.get('HTTP_REFERER') or request.environ.get('HTTP_HOST')
        if not origin.startswith('http://') and not origin.startswith('https://'):
            origin = f'http://{origin}'
        g.table_visibility = 'all' if origin in API_ALLOWED_ORIGINS else 'hidden'
    except Exception as e:
        API_LOGGER.warning(f'Error checking hidden table permission: {e}')
        g.table_visibility = 'hidden'
        
@app.before_request
def check_allowed_method():
    if request.method not in API_REQUEST_METHODS:
        return json_result(False, API_STATUS_MESSAGES['invalid_method'](request.method, API_REQUEST_METHODS, f'Request method {request.method} is not allowed.'))

@app.before_request
def check_content_type():
    if not request.content_type and request.method in API_DATA_METHODS:
        data_types = [ct.split('/')[-1].upper() for ct in API_VALID_CONTENT_TYPES]
        return json_result(False, API_STATUS_MESSAGES['no_content_type'](data_types))
    
    if request.method in API_DATA_METHODS and str(request.content_type.split(';')[0]).lower() not in API_VALID_CONTENT_TYPES:
        return json_result(False, API_STATUS_MESSAGES['invalid_content_type'](str(request.content_type), API_VALID_CONTENT_TYPES))
        
@app.before_request
def check_data_exists():
    if request.method in API_DATA_METHODS and not request.json:
        APP_LOGGER.warning(f'No data provided for request: {request.url}')
        return json_result(False, API_STATUS_MESSAGES['no_data_provided'](API_VALID_CONTENT_TYPES))
        
@app.before_request
def restrict_methods_for_disallowed_origins():
    try:
        origin = request.environ.get('HTTP_ORIGIN') or request.environ.get('HTTP_REFERER') or request.environ.get('HTTP_HOST')
        if not origin.startswith('http://') and not origin.startswith('https://'):
            origin = f'http://{origin}'
        
        if origin not in API_ALLOWED_ORIGINS and request.method != 'GET':
            return json_result(False, API_STATUS_MESSAGES['origin_not_allowed'])
    except Exception as e:
        return json_result(False, API_STATUS_MESSAGES['software_error'](str(e)))
    
# ------------------------------------- #
# Error handlers                        #
# ------------------------------------- #
@app.errorhandler(400)
def bad_request(error):
    return json_result(False, API_STATUS_MESSAGES['bad_request'](str(error)))

@app.errorhandler(404)
def not_found(error):
    return json_result(False, API_STATUS_MESSAGES['not_found'](request.url, str(error)))

@app.errorhandler(405)
def method_not_allowed(error):
    return json_result(False, API_STATUS_MESSAGES['invalid_method'](request.method, API_REQUEST_METHODS, str(error)))

@app.errorhandler(429)
def too_many_requests(error):
    return json_result(False, API_STATUS_MESSAGES['too_many_requests'](str(error), f'{API_CONFIG["limits"]["per_minute"]}/minute'))

@app.errorhandler(500)
def internal_error(error):
    return json_result(False, API_STATUS_MESSAGES['software_error'](str(error)))

# ------------------------------------- #
# GET - routes                          #
# ------------------------------------- #
@app.get(f'{API_CORE_URL_PREFIX}/<table>')
def select_all(table):
    route = GetRoute(db, f'{API_CORE_URL_PREFIX}/{table}', DB_LOGGER, API_LOGGER)
    return route.get_all(table)

@app.get(f'{API_CORE_URL_PREFIX}/<table>/', defaults={'id': None})
@app.get(f'{API_CORE_URL_PREFIX}/<table>/<id>')
def select_one(table, id):
    route = GetRoute(db, f'{API_CORE_URL_PREFIX}/{table}/{id}', DB_LOGGER, API_LOGGER)
    return route.get_one(table, id) 

# ------------------------------------- #
# POST - routes                         #
# ------------------------------------- #
@app.post(f'{API_CORE_URL_PREFIX}/<table>')
def insert(table):
    route = PostRoute(db, f'{API_CORE_URL_PREFIX}/{table}', DB_LOGGER, API_LOGGER)
    return route.insert_one(table)

# ------------------------------------- #
# PUT - routes                          #
# ------------------------------------- #
@app.put(f'{API_CORE_URL_PREFIX}/<table>/<id>')
def update(table, id):
    route = PutRoute(db, f'{API_CORE_URL_PREFIX}/{table}/{id}', DB_LOGGER, API_LOGGER)
    return route.update_one(table, id)

# ------------------------------------- #
# PATCH - routes                        #
# ------------------------------------- #
@app.patch(f'{API_CORE_URL_PREFIX}/<table>/<id>')
def patch(table, id):
    # Virtually same logic as PUT
    route = PutRoute(db, f'{API_CORE_URL_PREFIX}/{table}/{id}', DB_LOGGER, API_LOGGER)
    return route.update_one(table, id)

# ------------------------------------- #
# DELETE - routes                       #
# ------------------------------------- #
@app.delete(f'{API_CORE_URL_PREFIX}/<table>/<id>')
def delete(table, id):
    route = DeleteRoute(db, f'{API_CORE_URL_PREFIX}/{table}/{id}', DB_LOGGER, API_LOGGER)
    return route.delete_one(table, id)

# ------------------------------------- #
# HEAD - routes                         #
# ------------------------------------- #
@app.route(f'{API_CORE_URL_PREFIX}/<table>', methods=['HEAD'])
def head(table):
    route = GetRoute(db, f'{API_CORE_URL_PREFIX}/{table}', DB_LOGGER, API_LOGGER)
    return route.get_all(table, True)

@app.route(f'{API_CORE_URL_PREFIX}/<table>/<id>', methods=['HEAD'])
def head_one(table, id):
    route = GetRoute(db, f'{API_CORE_URL_PREFIX}/{table}/{id}', DB_LOGGER, API_LOGGER)
    return route.get_one(table, id, True)

# ------------------------------------- #
# Main function                         #
# ------------------------------------- #
if __name__ == '__main__':
    debug = APP_CONFIG.get('debug', True)
    app_env = APP_CONFIG.get('env', 'development')
    
    match app_env:
        case 'development':
            APP_LOGGER.info('API started in development mode.')
            app.run(debug = debug, port = API_CONFIG['port'])
        case 'production':
            APP_LOGGER.info('API started in production mode.')
            WAITRESS_LOGGER.info('Waitress server started.')
            
            from waitress import serve
            
            # TODO - this requires a bit of testing, cant run it locally (it atleast starts up though, which is good enough for now)
            serve(
                app = app, 
                host = WAITRESS_CONFIG['host'], 
                port = WAITRESS_CONFIG['port'], 
                threads = WAITRESS_CONFIG['threads']
            )
        case _:
            APP_LOGGER.error(f'Invalid environment variable. Exiting...')
            print(f'FATAL ERROR:Invalid APP_ENV.\nEdit the APP_ENV in the .env file to match one of the following values:\n{", ".join(APP_ENVS)}')
            exit(1)