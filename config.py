from dotenv import load_dotenv
import os

def database_config() -> dict:
    load_dotenv()
    
    return {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'database': os.getenv('DB_NAME')
    }
    
def app_config() -> dict:
    load_dotenv()
    
    return {
        'host': os.getenv('APP_HOST'),
        'port': os.getenv('APP_PORT'),
        'debug': os.getenv('APP_DEBUG')
    }
    
def api_config() -> dict:
    load_dotenv()
    
    return {
        'url': os.getenv('API_URL'),
        'key': os.getenv('API_CLIENT_ID'),
        'secret': os.getenv('API_CLIENT_SECRET')
    }