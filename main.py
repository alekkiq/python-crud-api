from flask import Flask, request, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv

from config import database_config, api_config, app_config
from utils.rest_utils import *
from Logger import Logger
from Database import Database, DatabaseManager

# Routes
from Routes.routes.Get import Get
from Routes.routes.Post import Post
from Routes.routes.Put import Put
from Routes.routes.Delete import Delete

config = api_config()

# Start the Logger
logger = Logger().get_logger()

# Initialize the Database, and the DatabaseManager
database = Database(database_config(), logger)
db = DatabaseManager(database, logger)

# Initialize the Flask app
app = Flask(app_config().get('name', __name__))
api_url = config.get('url')

# Define valid CORS origins
cors_origins = config.get('allowed_origins', [])

# Enable CORS
CORS(app, resources={r"/*": {"origins": cors_origins}}, supports_credentials=True)

# Avoid favicon.ico requests
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.before_request
def check_allowed_origin():
    '''
    Checks if the request origin is allowed in hidden tables, and sets the table visibility accordingly.
    '''
    try:
        origin = request.environ.get('HTTP_ORIGIN')
        if origin in cors_origins:
            g.table_visibility = 'all'
        else:
            g.table_visibility = 'hidden'
    except Exception as e:
        logger.error(f'Error checking hidden tables: {e}')
        g.table_visibility  = 'hidden'

# ------------------------------
# GET routes
# ------------------------------
@app.get('/<table>')
def select_all(table):
    route = Get(db = db, path = f'/{table}')
    return route.select_all(table)

@app.get('/<table>/', defaults={'id': None})
@app.get('/<table>/<id>')
def select_one(table, id):
    route = Get(db = db, path = f'/{table}/{id}')
    return route.select_one(table, id)


# ------------------------------
# POST routes
# ------------------------------

    
if __name__ == '__main__':
    debug = app_config().get('debug', True)
    app.run(debug=debug, port=5000)