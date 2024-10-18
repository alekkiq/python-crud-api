# Python deps & external libraries
from abc import ABC, abstractmethod
from datetime import datetime, timezone

# Imports for proper typing
from Logger import Logger

# Status messages
from status import DATABASE_STATUS_MESSAGES as STATUS_MESSAGES

# Constants
from constants import API_CORE_URL_PREFIX

class Database(ABC):
    '''
    Core abstract class for database instances. This class should be inherited by the database engine classes.
    
    Attributes:
        config (dict): The database connection options
        logger (Logger): The logger instance
    '''
    def __init__(self, config: dict, logger: Logger, db_type: str):
        self.logger = logger
        self.config = config
        self.connection = self._create_connection()
        self.db_type = db_type if db_type else self.__class__.__name__.replace('Database', '').lower()
        
        # Define valid SQL actions
        self.valid_sql_actions = ('select', 'insert', 'update', 'delete')
        self.committable_actions = ('insert', 'update', 'delete')
        
    @abstractmethod
    def _create_connection(self) -> any:
        '''
        Create a connection to the database. This method should be implemented by the db-type classes accordingly.
        '''
        pass
        
    @abstractmethod
    def query(self, query: str, table_name: str = None, cursor_settings: dict = None, query_arguments: dict = None, is_meta_query: bool = False, with_body: bool = True) -> dict:
        '''
        The core method to execute a query on the database.
        
        Args:
            query (str): The query string
            table_name (str): The table name
            cursor_settings (dict): The cursor settings
            query_arguments (dict): The query arguments
            is_meta_query (bool): If the query is a meta query or not
            with_body (bool): If the query result should include the body or not
        '''
        pass
    
    def _commit_changes(self, query: str) -> dict:
        '''
        Checks if `query` is a committable action and commits the changes to the database.
        
        Args:
            query (str): The query string
        
        Returns:
            dict: The query result dictionary
        '''
        try:
            query_action = query.strip().lower().split(' ')[0]
            if query_action not in self.committable_actions:
                return # do not commit changes if the query is not committable (SELECT)
            self.connection.commit()
            self.logger.info(f'Changes committed to the database: {query}')
        except Exception as e:
            self.logger.error(f'Failed to commit changes to the database: {query}. Error: {str(e)}')
    
    def _build_get_query_result(self, query: str, table_name: str, query_arguments: dict, is_meta_query: bool = False, status: dict = {'success': True, 'type': 'info'}, affected_rows: int = 0, result_group: bool = False, data: list = [], with_body: bool = True) -> dict:
        '''
        Constructs the query result dictionary.
        
        Args:
            query (str): The query string
            table_name (str): The name of the table for constructing dynamic links
            query_arguments (dict): The query arguments
            status (dict): The query status
            affected_rows (int): The number of affected rows
            result_group (bool): If there are results or not
            data (list): The query result data
            is_meta_query (bool): If the query is a meta query or not
        
        Returns:
            dict: The query result dictionary. This dictionary ultimately appears in the API responses.
        '''
        # if the query is a meta query, return a simpler result immediately
        # for example, when querying the primary key of a table.
        if is_meta_query:
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
                'data': data,
            }
        
        # construct metadata
        total_records = len(data)
        limit = int(query_arguments.get('limit', -1))
        offset = int(query_arguments.get('offset', 0))
        
        if limit == -1:
            per_page = total_records
            page = 1
            total_pages = 1
        else:
            per_page = limit
            page = (offset // limit) + 1
            total_pages = (total_records + per_page - 1) // per_page

        base_url = f'{API_CORE_URL_PREFIX}/{table_name}'
        self_url = base_url
        next_url = None
        prev_url = None

        # add query parameters to links if limit is not -1
        if limit != -1:
            self_url += f'?offset={offset}&limit={limit}'
            if page < total_pages:
                next_url = f'{base_url}?offset={offset + limit}&limit={limit}'
            if page > 1:
                prev_url = f'{base_url}?offset={max(0, offset - limit)}&limit={limit}'

        # construct the final dictionary
        return {
            'success': status.get('success'),
            'status': {
                'success': status.get('success'),
                'type': status.get('type')
            },
            'affected_rows': affected_rows,
            'result_group': result_group,
            'query': {
                'sql': {
                    'statement': query.get('query'),
                    'type': query.get('type')
                },
                'arguments': query_arguments
            },
            'data': data if with_body else 'Request method does not include a body in the response.',
            'meta': {
                'total_records': total_records,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages
            },
            'links': {
                'self': self_url,
                'next': next_url,
                'prev': prev_url
            },
            'timestamp': {
                'utc': datetime.now(timezone.utc).isoformat(),
            }
        }