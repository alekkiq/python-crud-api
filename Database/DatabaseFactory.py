# Imports for proper typing
from . import Database
from Logger import Logger

# Constants
from constants import ALLOWED_DATABASES

class DatabaseFactory:
    @staticmethod
    def create_database(config: dict, logger: Logger) -> Database:
        '''
        Creates a new database object based on `config`.
        
        Args:
            database_type (str): The database type
        '''
        database_type = config.get('type', 'mysql')
        
        if database_type not in ALLOWED_DATABASES:
            raise ValueError(f'Database type {database_type} is not allowed.')
        else: 
            match database_type:
                case 'mysql':
                    from .engines import MySQLDatabase
                    return MySQLDatabase(config, logger)
                case 'postgresql':
                    from .engines import PostgreSQLDatabase
                    return PostgreSQLDatabase(config, logger)
                case 'sqlite':
                    from .engines import SQLiteDatabase
                    return SQLiteDatabase(config, logger)
                case _:
                    logger.error(f'Database type {database_type} is not supported.')
                    raise ValueError(f'Database type {database_type} is not supported.')