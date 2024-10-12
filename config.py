from dotenv import load_dotenv
import os

load_dotenv()

def database_config() -> dict:
    '''
    Gets the database configuration from the environment variables
    
    Returns:
        dict: The database connection options
    '''
    return {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'database': os.getenv('DB_DATABASE'),
        'autocommit': os.getenv('DB_AUTOCOMMIT', False),
    }
    
def api_config() -> dict:
    '''
    Gets the API configuration from the environment variables
    
    Returns:
        dict: The API configuration keys
    '''
    return {
        'url': os.getenv('API_URL'),
        'key': os.getenv('API_CLIENT_ID'),
        'secret': os.getenv('API_CLIENT_SECRET'),
        'allowed_origins': os.getenv('API_ALLOWED_ORIGINS', []).split(','),
        'hidden_tables': os.getenv('API_HIDDEN_TABLES', []).split(',')
    }
    
def app_config() -> dict:
    '''
    Gets the application configuration from the environment variables
    
    Returns:
        dict: The application keys
    '''
    return {
        'name': os.getenv('APP_NAME'),
        'env': os.getenv('APP_ENV', 'development'),
        'debug': os.getenv('APP_DEBUG', True),
        'version': os.getenv('APP_VERSION', '1.0.0')
    }