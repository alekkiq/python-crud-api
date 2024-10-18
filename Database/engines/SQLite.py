# Python deps & external libraries
import sqlite3

# Imports for proper typing
from typing import override
from Logger import Logger

from .. import Database
from status import DATABASE_STATUS_MESSAGES

class SQLiteDatabase(Database):
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
        super().__init__(config, logger, 'sqlite')
    
    @override
    def _create_connection(self) -> sqlite3.Connection:
        '''
        Create a connection to the MySQL database.
        
        Returns:
            sqlite3.Connection: The database connection object
        '''
        try:
            if not self.config['database'].endswith('.db'):
                self.config.get('database') = self.config['database'] + '.db'
            
            connection = sqlite3.connect(
                database            = self.config['database'],
                check_same_thread   = False
            )
            self.logger(DATABASE_STATUS_MESSAGES['connection_success'](self.config, 'SQLite')['message'], 'info')
            
            return connection
        except sqlite3.Error as e:
            raise RuntimeError(DATABASE_STATUS_MESSAGES['connection_fail'](self.config.get('database'), self.config, e)['message'])
        
    @override
    def query(self, query: str, table_name: str = None, cursor_settings: dict = None, query_arguments: dict = None, is_meta_query: bool = False, with_body: bool = True) -> dict:
        '''
        Execute `query` on the SQLite database.
        
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
            # Apply cursor settings if provided
            if cursor_settings:
                if cursor_settings.get('row_factory') == 'dict':
                    self.connection.row_factory = sqlite3.Row
                
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            result = None
            
            if with_body:
                result = cursor.fetchall()
            
            # Commit changes if necessary
            self._commit_changes(query)
        except sqlite3.Error as e:
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
                affected_rows = len(result),
                result_group = len(result) > 0,
                data = result,
                with_body = with_body
            )         