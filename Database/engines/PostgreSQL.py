import psycopg2
from psycopg2.extras import RealDictCursor

# Imports for proper typing
from typing import override
from Logger import Logger

from .. import Database
from STATUS import DATABASE_STATUS_MESSAGES

class PostgreSQLDatabase(Database):
    '''
    Database type: PostgreSQL
    '''
    def __init__(self, config: dict, logger: Logger):
        '''
        Initialize the PostgreSQL database object.
        
        Args:
            config (dict): The database connection options
            logger (Logger): The logger instance
        '''
        super().__init__(config, logger)
        
    @override
    def _create_connection(self) -> psycopg2.connect:
        '''
        Create a connection to the PostgreSQL database.
        
        Returns:
            psycopg2.connect: The database connection object
        '''
        try:
            connection = psycopg2.connect(
                host = self.config['host'],
                port = self.config['port'],
                user = self.config['user'],
                password = self.config['password'],
                database = self.config['database']
            )
            
            # Set auto-commit
            if self.config.get('autocommit', False):
                connection.autocommit = True
             
            # Set charset   
            if 'charset' in self.config:
                connection.set_client_encoding(self.config['charset'])
            
            self.logger.info(DATABASE_STATUS_MESSAGES['connection_success'](self.config, 'PostgreSQL')['message'])
        except psycopg2.Error as e:
            self.logger.error(DATABASE_STATUS_MESSAGES['connection_fail'](self.config, e)['message'])
            connection = None
        finally:
            return connection
        
    @override
    def query(self, query: str, table_name: str = None, cursor_settings: dict = None, query_arguments: dict = None) -> dict:
        '''
        Execute a query on the MySQL database.
        
        Args:
            query (str): The query string
            cursor_settings (dict): The cursor settings
            query_arguments (dict): The query arguments
        '''
        if self.connection is None:
            return DATABASE_STATUS_MESSAGES['connection_fail'](self.config, 'No connection established.')
        
        result = []
        status = {
            'success': True,
            'type': 'info'
        }
        
        try:
            cursor_factory = RealDictCursor if cursor_settings.get('dictionary', False) else None
            self.cursor = self.connection.cursor(cursor_factory = cursor_factory)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.logger.info(DATABASE_STATUS_MESSAGES['query_success'](query)['message'])
        except psycopg2.OperationalError as e:
            self.connection.rollback()
            status = {'success': False, 'type': 'error'}
            self.logger.error(DATABASE_STATUS_MESSAGES['query_fail'](query, e)['message'])
        finally:
            return self._build_get_query_result(
                query = query,
                table_name = table_name,
                query_arguments = query_arguments,
                status = status,
                affected_rows = self.cursor.rowcount,
                result_group = self.cursor.description is not None,
                data = result
            )