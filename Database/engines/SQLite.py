import sqlite3

# Imports for proper typing
from typing import override
from Logger import Logger

from .. import Database
from ..status_codes import DATABASE_STATUS_MESSAGES

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
        super().__init__(config, logger)
    
    @override
    def _create_connection(self) -> sqlite3.Connection:
        '''
        Create a connection to the MySQL database.
        
        Returns:
            sqlite3.Connection: The database connection object
        '''
        try:
            if not self.config['database'].endswith('.db'):
                self.config['database'] = self.config['database'] + '.db'
            
            connection = sqlite3.connect(
                database = self.config['database'], 
                autocommit = self.config['autocommit'],
                check_same_thread = False
            )
            self._log(DATABASE_STATUS_MESSAGES['connection_success'](self.config, 'SQLite')['message'], 'info')
        except sqlite3.Error as e:
            self._log(DATABASE_STATUS_MESSAGES['connection_fail'](self.config, e)['message'], 'error')
            connection = None
        finally:
            return connection
        
    @override
    def query(self, query: str, table_name: str = None, cursor_settings: dict = None, query_arguments: dict = None) -> dict:
        '''
        Execute a query on the SQLite database.
        
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
            self._log(f'Executing query: {query}', 'info')
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self._log(DATABASE_STATUS_MESSAGES['query_success'](str(self.cursor.statement))['message'], 'info')
        except sqlite3.Error as e:
            self.connection.rollback()
            status = {'success': False, 'type': 'error'}
            self._log(DATABASE_STATUS_MESSAGES['query_fail'](str(self.cursor.statement), e)['message'], 'error')   
        finally:
            return self._build_query_result(
                query = query,
                table_name = table_name,
                query_arguments = query_arguments,
                status = status,
                affected_rows = len(result),
                result_group = True if result else False,
                data = result
            )         