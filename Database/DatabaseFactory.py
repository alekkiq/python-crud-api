# Import all the engines
from .engines.MySQL import MySQLDatabase
from .engines.SQLite import SQLiteDatabase
from .engines.PostgreSQL import PostgreSQLDatabase

# Imports for proper typing
from .Database import Database
from Logger.Logger import Logger

# Constants
from constants import ALLOWED_DATABASES

class DatabaseFactory:
    @staticmethod
    def create_database(config: dict, logger: Logger) -> Database:
        '''
        Creates a new database object based on the configuration.
        
        Args:
            database_type (str): The database type
        '''
        database_type = config.get('type', 'mysql')
        
        if database_type not in ALLOWED_DATABASES:
            raise ValueError(f'Database type {database_type} is not allowed.')
        else: 
            match database_type:
                case 'mysql':
                    return MySQLDatabase(config, logger)
                case 'postgresql':
                    return PostgreSQLDatabase(config, logger)
                case 'sqlite':
                    return SQLiteDatabase(config, logger)
                case _:
                    logger.error(f'Database type {database_type} is not supported.')
                    raise ValueError(f'Database type {database_type} is not supported.')