from dotenv import load_dotenv
import os
from utils import ParseUtils
from constants import API_LOGGER, DB_LOGGER, WAITRESS_LOGGER

load_dotenv('.env')

# APP config
APP_CONFIG = {
    'name': os.getenv('APP_NAME'),
    'env': os.getenv('APP_ENV', 'development'),
    'debug': os.getenv('APP_DEBUG', True),
    'version': os.getenv('APP_VERSION', '1.0.0')
}

# Database config
DATABASE_CONFIG = {
    'type': os.getenv('DB_CONNECTION', 'mysql'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_DATABASE'),
    'autocommit': os.getenv('DB_AUTOCOMMIT', False),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    'collation': os.getenv('DB_COLLATION', 'utf8mb4_unicode_ci')
}

# API config
API_URL = os.getenv('API_URL')
API_CONFIG = {
    'url': API_URL,
    'id': os.getenv('API_CLIENT_ID'),
    'secret': os.getenv('API_CLIENT_SECRET'),
    'keys': os.getenv('API_KEYS', '').split(','),
    'secrets': ParseUtils.parse_secrets(os.getenv('API_SECRETS', ''), API_LOGGER),
    'allowed_origins': os.getenv('API_ALLOWED_ORIGINS', [API_URL]).split(','),
    'hidden_tables': os.getenv('API_HIDDEN_TABLES', []).split(',')
}

# Waitress config
WAITRESS_CONFIG = {
    'host': os.getenv('WAITRESS_HOST', None),
    'port': os.getenv('WAITRESS_PORT', None),
    'threads': os.getenv('WAITRESS_THREADS', None)
}