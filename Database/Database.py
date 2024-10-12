from abc import ABC, abstractmethod

class Database(ABC):
    '''
    Core abstract class for database instances. This class should be inherited by the database type classes (MySQL, Postgres, Mongo).
    
    Attributes:
        config (dict): The database connection options
        logger (Logger): The logger instance
    '''
    def __init__(self, config: dict, logger):
        self.__logger = logger
        self.config = config
        self.connection = self._create_connection()
        self.cursor = self.connection.cursor()
        
    @abstractmethod
    def _create_connection(self) -> any:
        '''
        Create a connection to the database. This method should be implemented by the db-type classes accordingly.
        '''
        pass
        
    @abstractmethod
    def query(self, query: str, cursor_settings: dict = None, query_arguments: dict = None) -> dict:
        '''
        The method to execute a query on the database.
        
        Args:
            query (str): The query string
            cursor_settings (dict): The cursor settings
            query_arguments (dict): The query arguments
        '''
        pass
    
    def _build_query_result(self, query: str, query_arguments: dict, status: dict = {'success': True, 'type': 'info'}, affected_rows: int = 0, result_group: bool = False, data: list = []) -> dict:
        '''
        Constructs the query result dictionary.
        
        Args:
            query (str): The query string
            query_arguments (dict): The query arguments
            status (dict): The query status
            affected_rows (int): The number of affected rows
            result_group (bool): If there are results or not
            data (list): The query result data
            
        Returns:
            dict: The query result dictionary. This dictionary ultimately appears in the API responses.
        '''
        return {
            'status': {
                'success': status.get('success', True),
                'type': status.get('type', 'info')
            },
            'affected_rows': affected_rows,
            'result_group': result_group,
            'query': {
                'statement': query,
                'arguments': query_arguments
            },
            'data': data
        } 
        
    def _log(self, message: str, level: str = 'info'):
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