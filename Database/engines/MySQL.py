# Python deps & external libraries
import mysql.connector

# Imports for proper typing
from typing import override
from Logger import Logger

from .. import Database
from status import DATABASE_STATUS_MESSAGES

class MySQLDatabase(Database):
    '''
    Database type: MySQL (MariaDB)
    '''
    def __init__(self, config: dict, logger: Logger):
        '''
        Initialize the MySQL database object.
        
        Args:
            config (dict): The database connection options
            logger (Logger): The logger instance
        '''
        super().__init__(config, logger, 'mysql')
    
    @override
    def _create_connection(self) -> mysql.connector.connection.MySQLConnection:
        '''
        Create a connection to the MySQL database.
        
        Returns:
            mysql.connector.connection.MySQLConnection: The database connection object
        '''
        try:
            connection = mysql.connector.connect(
                host        = self.config.get('host'),
                port        = self.config.get('port'),
                user        = self.config.get('user'),
                password    = self.config.get('password'),
                database    = self.config.get('database'),
                collation   = self.config.get('collation', 'utf8mb4_general_ci'),
                charset     = self.config.get('charset', 'utf8mb4'),
            )
            self.logger.info(DATABASE_STATUS_MESSAGES['connection_success'](connection.database, self.config, 'MySQL')['message'])
            
            return connection
        except mysql.connector.Error as e:
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
            cursor = self.connection.cursor(**cursor_settings)
            cursor.execute(query)

            result = None
            
            if with_body:
                result = cursor.fetchall()
            
            # Commit changes if necessary
            self._commit_changes(query)
        except mysql.connector.Error as e:
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
                result_group = cursor.with_rows is not False,
                data = result,
                with_body = with_body
            )