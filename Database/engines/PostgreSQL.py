# Python deps & external libraries
import psycopg2
from psycopg2.extras import RealDictCursor

# Imports for proper typing
from typing import override
from Logger import Logger

from .. import Database
from status import DATABASE_STATUS_MESSAGES

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
        super().__init__(config, logger, 'postgresql')
        
    @override
    def _create_connection(self) -> psycopg2.connect:
        '''
        Create a connection to the PostgreSQL database.
        
        Returns:
            psycopg2.connect: The database connection object
        '''
        try:
            connection = psycopg2.connect(
                host        = self.config.get('host'),
                port        = self.config.get('port'),
                user        = self.config.get('user'),
                password    = self.config.get('password'),
                database    = self.config.get('database'),
            )
             
            # Set charset   
            if 'charset' in self.config:
                connection.set_client_encoding(self.config.get('charset'))
            
            self.logger.info(DATABASE_STATUS_MESSAGES['connection_success'](self.config, 'PostgreSQL')['message'])
        
            return connection
        except psycopg2.Error as e:
            raise RuntimeError(DATABASE_STATUS_MESSAGES['connection_fail'](self.config.get('database'), self.config, e)['message'])
        
    @override
    def query(self, query: str, table_name: str = None, cursor_settings: dict = None, query_arguments: dict = None, is_meta_query: bool = False, with_body: bool = True) -> dict:
        '''
        Execute `query` on the MySQL database.
        
        Args:
            query (str): The query string
            cursor_settings (dict): The cursor settings
            query_arguments (dict): The query arguments
            is_meta_query (bool): If the query is a meta query or not
            with_body (bool): If the query result should include the body or not
            
        Returns:
            dict: The query result dictionary
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
            cursor = self.connection.cursor(cursor_factory = cursor_factory)
            cursor.execute(query)
            
            result = None
            
            if with_body:
                result = cursor.fetchall()
            
            # Commit changes if necessary
            self._commit_changes(query)
        except psycopg2.OperationalError as e:
            self.connection.rollback()
            status = DATABASE_STATUS_MESSAGES['query_fail'](e, query)
            self.logger.error(status['message'])
        finally:
            return self._build_get_query_result(
                query = {
                    'type': query.strip().lower().split(' ')[0],
                    'query': query
                },
                table_name = table_name,
                query_arguments = query_arguments,
                is_meta_query = is_meta_query,
                status = status,
                affected_rows = cursor.rowcount if cursor.rowcount != -1 else 0,
                result_group = cursor.description is not None,
                data = result,
                with_body = with_body
            )