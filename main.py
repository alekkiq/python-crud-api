# ------------------------------------
# Main file for running the API.
# ------------------------------------

# Python dependencies & external libraries
from flask import Flask, request, jsonify, g, abort
from flask_cors import CORS
from dotenv import load_dotenv

# Constants
# Configurations
from constants import DATABASE_CONFIG, API_CONFIG, APP_CONFIG
from constants import ALLOWED_ORIGINS, API_KEYS, API_SECRETS, API_CORE_URL_PREFIX

# Modules
from Logger.Logger import Logger
from Database.Factory import DatabaseFactory
from Database.Manager import DatabaseManager

# Routes
from Routes.routes.Get import Get as GetRoute

config = API_CONFIG()

# Start the Logger
logger = Logger().get_logger()

# Initialize the Database, and the DatabaseManager
database = DatabaseFactory.create_database(DATABASE_CONFIG(), logger)
db = DatabaseManager(database, logger)

# Initialize the Flask app
app = Flask(APP_CONFIG().get('name', __name__))
api_url = config.get('url')

# Enable CORS
CORS(app, resources={f'{API_CORE_URL_PREFIX}/*': {'origins': ALLOWED_ORIGINS}}, supports_credentials=True)

# Avoid favicon.ico requests
@app.route('/favicon.ico')
def favicon():
    return '', 204

# ------------------------------
# Middleware
# ------------------------------
@app.before_request
def check_api_key():
    api_key = request.headers.get('X-API-KEY')
    api_secret = request.headers.get('X-API-SECRET')
    
    if api_key not in API_KEYS or API_SECRETS.get(api_key) != api_secret:
        print('Invalid API key or secret')
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
        logger.error(f'Error checking hidden table permission: {e}')
        g.table_visibility = 'hidden'
        
# ------------------------------
# Error handlers
# ------------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'status': 404}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed', 'status': 405}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'status': 500}), 500

# ------------------------------
# GET routes
# ------------------------------
@app.get(f'{API_CORE_URL_PREFIX}/<table>')
def select_all(table):
    route = GetRoute(db, f'{API_CORE_URL_PREFIX}/{table}', logger)
    return route.get_all(table)

@app.get(f'{API_CORE_URL_PREFIX}/<table>/', defaults={'id': None})
@app.get(f'{API_CORE_URL_PREFIX}/<table>/<id>')
def select_one(table, id):
    route = GetRoute(db, f'{API_CORE_URL_PREFIX}/{table}/{id}', logger)
    return route.get_one(table, id)


# ------------------------------
# POST routes
# ------------------------------
# ...
    
if __name__ == '__main__':
    debug = APP_CONFIG().get('debug', True)
    app.run(debug=debug, port=5000)