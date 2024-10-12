import mysql.connector
from pypika import Query, Table, Field, Order

# Status codes & messages
from .status_codes import DATABASE_STATUS_MESSAGES as STATUS_MESSAGES

# TODO
# - Add support for other database engines
# - This class works with MySQL/MariaDB only

class Database:
    '''
    Database class is responsible for handling the common database actions.
    
    Attributes:
        config (dict): The database connection options
        logger (Logger): The logger instance
        connection (mysql.connector.connection.MySQLConnection): The database connection
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor
    '''
    def __init__(self, config: dict, logger):
        self.__config = config
        self.__logger = logger
        self.connection = self.__create_connection()
        self.cursor = self.connection.cursor()
    
    # ------------------------------
    # Private methods
    # ------------------------------
    def __create_connection(self) -> mysql.connector.connection.MySQLConnection:
        try:
            connection = mysql.connector.connect(
                host = self.__config['host'],
                port = self.__config['port'],
                user = self.__config['user'],
                password = self.__config['password'],
                database = self.__config['database'],
                autocommit = self.__config['autocommit'],
                collation = 'utf8mb4_unicode_ci',
                charset = 'utf8mb4'
            )
            self.__log(STATUS_MESSAGES['connection_success'](f'{self.__config['host']}:{self.__config['port']}')['message'], 'info')
            return connection
        except Exception as e:
            self.__log(STATUS_MESSAGES['connection_fail'](f'Configs: {self.__config}', e)['message'], 'error')
            return None
        
    def __log(self, message: str, level: str = 'info'):
        '''
        Logs a message
        
        Args:
            message (str): The message to log
            level (str): The log level
        '''
        match level:
            case 'info':
                self.__logger.info(message)
            case 'warning':
                self.__logger.warning(message)
            case 'error':
                self.__logger.error(message)
            case _:
                self.__logger.info(message)


    # ------------------------------
    # Public methods
    # ------------------------------
    def close(self):
        '''
        Closes the database connection
        '''
        self.cursor.close()
        self.connection.close()
    
    
    def query(self, query: str, query_arguments: dict = None, cursor_settings: dict = None) -> dict:
        '''
        Executes a query and returns the result
        
        Args:
            query (str): The ready SQL query to execute
            cursor_settings (dict): The cursor settings
        '''
        self.__logger.info(f'Executing query: `{query}`')
        
        try:
            cursor = self.connection.cursor(dictionary = cursor_settings.get('dictionary', False))
            cursor.execute(query)
            
            # Log the query execution
            self.__log(STATUS_MESSAGES['query_success'](str(cursor.statement))['message'], 'info')
            
            data_found = cursor.fetchall()
            result = {
                'status': {
                    'success': True,
                    'type': 'info'
                },
                'affected_rows': cursor.rowcount,
                'result_group': cursor.with_rows,
                'query': {
                    'statement': cursor.statement,
                    'arguments': query_arguments
                },
                'data': data_found
            }
        except Exception as e:
            # Log the query error
            self.__log(STATUS_MESSAGES['query_error'](e, str(cursor.statement))['message'], 'error')
            
            result = {
                'status': {
                    'success': False,
                    'type': 'error'
                },
                'affected_rows': cursor.rowcount,
                'result_group': cursor.with_rows,
                'query': {
                    'statement': cursor.statement,
                    'arguments': query_arguments
                },
                'data': []
            }
        finally:
            return result 