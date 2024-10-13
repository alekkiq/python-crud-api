# ------------------------------------- #
#                                       #
# Main file for running the API.        #
#                                       #
# ------------------------------------ -#

# Python dependencies & external libraries
from flask import Flask, request, jsonify, g, abort
from flask_cors import CORS

# ------------------------------------- #
# Constants & configurations            #
# ------------------------------------- #

# Configurations
from config import DATABASE_CONFIG, API_CONFIG, APP_CONFIG, WAITRESS_CONFIG
from constants import APP_ENVS, API_CORE_URL_PREFIX, initialize_api_constants

# Initialize API constants
initialize_api_constants(API_CONFIG)
from constants import API_KEYS, API_SECRETS, ALLOWED_ORIGINS, HIDDEN_TABLES

# Logger
from constants import APP_LOGGER, DB_LOGGER, API_LOGGER, WAITRESS_LOGGER

# Modules
from Database.Factory import DatabaseFactory
from Database.Manager import DatabaseManager

# Routes
from Routes.routes.Get import Get as GetRoute

# Create the Database instance and the DatabaseManager
database = DatabaseFactory.create_database(DATABASE_CONFIG, DB_LOGGER)
db = DatabaseManager(database, DB_LOGGER)

# Initialize the Flask app
app = Flask(APP_CONFIG.get('name', __name__))
api_url = API_CONFIG.get('url', 'http://localhost:5000')

# Enable CORS
CORS(
    app = app, 
    resources = {
        f'{API_CORE_URL_PREFIX}/*': {
                'origins': ALLOWED_ORIGINS
            }
        }, 
    supports_credentials = True
)

# Avoid favicon.ico requests errors
@app.route('/favicon.ico')
def favicon():
    return '', 204

# ------------------------------------- #
# Middleware (before_request)           #
# ------------------------------------- #
@app.before_request
def check_api_key():
    api_key = request.headers.get('X-API-KEY')
    api_secret = request.headers.get('X-API-SECRET')
    
    if api_key not in API_KEYS or API_SECRETS.get(api_key) != api_secret:
        APP_LOGGER.warning(f'Unauthorized request: {request.url}')
        abort(403)  # Forbidden request
        
@app.before_request
def check_allowed_origin():
    '''
    Checks if the request origin is allowed in hidden tables, and sets the table visibility accordingly.
    '''
    try:
        origin = request.environ.get('HTTP_ORIGIN') or request.environ.get('HTTP_REFERER') or request.environ.get('HTTP_HOST')
        if not origin.startswith('http://') and not origin.startswith('https://'):
            origin = f'http://{origin}'
        g.table_visibility = 'all' if origin in ALLOWED_ORIGINS else 'hidden'
    except Exception as e:
        API_LOGGER.error(f'Error checking hidden table permission: {e}')
        g.table_visibility = 'hidden'
        
# ------------------------------------- #
# Error handlers                        #
# ------------------------------------- #
@app.errorhandler(404)
def not_found(error):
    APP_LOGGER.error(f'404 error: {request.url}')
    return jsonify({'error': 'Not found', 'status': 404}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    APP_LOGGER.error(f'404 error: {request.url}')
    return jsonify({'error': 'Method not allowed', 'status': 405}), 405

@app.errorhandler(500)
def internal_error(error):
    APP_LOGGER.error(f'404 error: {request.url}')
    return jsonify({'error': 'Internal server error', 'status': 500}), 500

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
# ...

# ------------------------------------- #
# PUT - routes                          #
# ------------------------------------- #

# ------------------------------------- #
# DELETE - routes                       #
# ------------------------------------- #
    
    
# ------------------------------------- #
# Main function                         #
# ------------------------------------- #
if __name__ == '__main__':
    debug = APP_CONFIG.get('debug', True)
    app_env = APP_CONFIG.get('env', 'development')
    
    match app_env:
        case 'development':
            APP_LOGGER.info('API started in development mode.')
            app.run(debug = debug, port=5000)
        case 'production':
            APP_LOGGER.info('API started in production mode.')
            WAITRESS_LOGGER.info('Waitress server started.')
            
            from waitress import serve
            
            # TODO - this requires a bit of testing, cant run it locally (it atleast starts up though, which is good enough for now)
            serve(
                app = app, 
                host=WAITRESS_CONFIG['host'], 
                port=WAITRESS_CONFIG['port'], 
                threads=WAITRESS_CONFIG['threads']
            )
        case _:
            APP_LOGGER.error(f'Invalid environment variable. Exiting...')
            print(f'FATAL ERROR:Invalid APP_ENV.\nEdit the APP_ENV in the .env file to match one of the following values:\n{", ".join(APP_ENVS)}')
            exit(1)