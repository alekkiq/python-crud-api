from .engines.MySQL import MySQLDatabase
from .engines.SQLite import SQLiteDatabase

class DatabaseFactory:
    ALLOWED_DATABASES = ('mysql', 'postgresql', 'mongodb', 'sqlite')
    
    @staticmethod
    def create_database(config: dict, logger):
        '''
        Creates a new database object based on the configuration.
        
        Args:
            database_type (str): The database type
        '''
        database_type = config.get('type', 'mysql')
        
        if database_type not in DatabaseFactory.ALLOWED_DATABASES:
            raise ValueError(f'Database type {database_type} is not allowed.')
        else: 
            match database_type:
                case 'mysql':
                    return MySQLDatabase(config, logger)
                case 'postgresql':
                    pass
                case 'sqlite':
                    return SQLiteDatabase(config, logger)
                case _:
                    raise ValueError(f'Database type {database_type} is not supported.')