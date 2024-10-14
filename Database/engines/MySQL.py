# Python deps & external libraries
import mysql.connector

# Imports for proper typing
from typing import override
from Logger import Logger

from .. import Database
from STATUS import DATABASE_STATUS_MESSAGES

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
        super().__init__(config, logger)
    
    @override
    def _create_connection(self) -> mysql.connector.connection.MySQLConnection:
        '''
        Create a connection to the MySQL database.
        
        Returns:
            mysql.connector.connection.MySQLConnection: The database connection object
        '''
        try:
            connection = mysql.connector.connect(
                host = self.config['host'],
                port = self.config['port'],
                user = self.config['user'],
                password = self.config['password'],
                database = self.config['database'],
                autocommit = self.config['autocommit'],
                collation = 'utf8mb4_unicode_ci',
                charset = 'utf8mb4'
            )
            self.logger.info(DATABASE_STATUS_MESSAGES['connection_success'](self.config, 'MySQL')['message'])
        except mysql.connector.Error as e:
            self.logger.error(DATABASE_STATUS_MESSAGES['connection_fail'](self.config, e)['message'])
            connection = None
        finally:
            return connection
        
    @override
    def query(self, query: str, table_name: str = None, cursor_settings: dict = None, query_arguments: dict = None, is_meta_query: bool = False) -> dict:
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
            self.cursor = self.connection.cursor(**cursor_settings)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            
            # Commit changes if necessary
            self._commit_changes(query)
            
            self.logger.info(DATABASE_STATUS_MESSAGES['query_success'](query)['message'])
        except mysql.connector.Error as e:
            self.connection.rollback()
            status = {'success': False, 'type': 'error'}
            self.logger.error(DATABASE_STATUS_MESSAGES['query_fail'](query, e)['message'])
        finally:
            return self._build_get_query_result(
                query = query,
                table_name = table_name,
                query_arguments = query_arguments,
                is_meta_query = is_meta_query,
                status = status,
                affected_rows = self.cursor.rowcount,
                result_group = self.cursor.with_rows,
                data = result
            )