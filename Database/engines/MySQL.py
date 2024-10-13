import mysql.connector

from typing import override

from ..Database import Database
from ..status_codes import DATABASE_STATUS_MESSAGES

class MySQLDatabase(Database):
    '''
    Database type: MySQL (MariaDB)
    '''
    def __init__(self, config: dict, logger):
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
            self._log(DATABASE_STATUS_MESSAGES['connection_success'](self.config, 'MySQL')['message'], 'info')
        except mysql.connector.Error as e:
            self._log(DATABASE_STATUS_MESSAGES['connection_fail'](self.config, e)['message'], 'error')
            connection = None
        finally:
            return connection
        
    @override
    def query(self, query: str, cursor_settings: dict = None, query_arguments: dict = None) -> dict:
        '''
        Execute a query on the MySQL database.
        
        Args:
            query (str): The query string
            cursor_settings (dict): The cursor settings
            query_arguments (dict): The query arguments
        '''
        if self.connection is None:
            return DATABASE_STATUS_MESSAGES['connection_fail'](self.__config, 'No connection established.')
        
        result = []
        status = {}
        
        try:
            self.cursor = self.connection.cursor(**cursor_settings)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            status = {
                'success': True if result else False,
                'type': 'info' if result else 'warning'
            }
            self._log(DATABASE_STATUS_MESSAGES['query_success'](query)['message'], 'info')
        except mysql.connector.Error as e:
            self.connection.rollback()
            status = {'success': False, 'type': 'error'}
            self._log(DATABASE_STATUS_MESSAGES['query_fail'](query, e)['message'], 'error')
        finally:
            return self._build_query_result(
                query = query,
                query_arguments = query_arguments,
                status = status,
                affected_rows = self.cursor.rowcount,
                result_group = self.cursor.with_rows,
                data = result
            )