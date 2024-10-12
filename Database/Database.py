import mysql.connector
from pypika import Query, Table, Field, Order

# Status codes & messages
from .status_codes import DATABASE_STATUS_CODES as STATUS_CODES, DATABASE_STATUS_MESSAGES as STATUS_MESSAGES

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
            
            self.__logger.info(f'Database connection opened at `{self.__config["host"]}:{self.__config["port"]}`')
            return connection
        except Exception as e:
            self.__logger.error(f'Error establishing database connection: {e}')
            return None
        
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
            
            self.__logger.info(f'Query executed successfully')
            
            data_found = cursor.fetchall()
            
            return {
                'success': True,
                'affected_rows': cursor.rowcount,
                'query': cursor.statement,
                'arguments': query_arguments,
                'result_group': len(data_found) > 0,
                'data': data_found
            }
        except Exception as e:
            self.__logger.error(f'Error executing query: {e}')
            return {
                'success': False,
                'error': str(e)
            }