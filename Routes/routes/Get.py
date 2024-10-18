# Python deps & external libraries
import flask
from flask import jsonify, request, g

# The abstract class for the routes
from .. import Route

# Imports for proper typing
from Logger import Logger
from Database import DatabaseManager

# Constants
from constants import API_VALID_QUERY_ARGS, API_PROTECTED_TABLES

class Get(Route):
    '''
    Handles the GET requests for the API.
    
    Attributes:
        db_manager (DatabaseManager): The database manager
        path (str): The route path
        db_logger (Logger): The database logger instance
        api_logger (Logger): The API logger instance
    '''
    def __init__(self, db_manager: DatabaseManager, path: str, db_logger: Logger, api_logger: Logger):
        super().__init__(db_manager, db_logger, api_logger, path, 'GET')
                
    def _offset_without_limit_condition(self, query_args: dict) -> bool:
        '''
        Checks if the query has an offset argument without a limit.
        '''
        return 'offset' in query_args and 'limit' not in query_args

    def _remove_offset_action(self, query_args: dict):
        '''
        Removes the offset argument from the query arguments.
        '''
        del query_args['offset']
        
    def _limit_is_zero_condition(self, query_args: dict) -> bool:
        '''
        Checks if the limit is set to zero (or -1).
        '''
        return 'limit' in query_args and (query_args['limit'] == '0' or query_args['limit'] == '-1')
       
    def _set_limit_to_none_action(self, query_args: dict):
        '''
        Sets the limit to None.
        
        Args:
            query_args (dict): The query arguments
        '''
        query_args['limit'] = None   
    
    def _get(self, table: str, query_args: dict, pk: str = None, with_body: bool = True):
        '''
        Common logic for handling GET requests.
        
        Args:
            table (str): The table name
            query_args (dict): The query arguments
            pk (str, optional): The primary key value. Defaults to None.
        '''
        if self._before_db_action(table, query_args):
            return self._before_db_action(table, query_args)
        
        query_args = self._parse_query_args(request, API_VALID_QUERY_ARGS['GET'], table)
        
        if pk is not None:
            primary_key = self.db_manager.primary_key(table)
            if primary_key is None:
                return jsonify({'error': 'Primary key not found'}), 400
            query_args['where'] = f'{primary_key} = {pk}'
        
        # Handle query exceptions
        rules = [
            { # Remove offset if limit is not provided
                'condition': self._offset_without_limit_condition, 
                'action': self._remove_offset_action
            }, 
            { # Set limit to None if limit is 0 or -1 (bypass hardcoded default limit)
                'condition': self._limit_is_zero_condition,
                'action': self._set_limit_to_none_action
            }
            # ... add more rules here
        ]
        self._handle_query_exceptions(query_args, rules)
        
        result = self.db_manager.select(
            table_name=table, 
            fields=['*'], 
            query_args=query_args,
            with_fetch = True
        )
        
        return jsonify(result)
    
    def get_all(self, table: str, head: bool = True):
        '''
        Handles the GET requests for ALL database records in the API.
        
        Args:
            table (str): The table name
            head (bool): Whether to include the body in the response
        '''
        return self._get(
            table = table, 
            query_args = request.args,
            with_body = head
        )

    def get_one(self, table: str, pk: str, head: bool = True):
        '''
        Handles the GET requests for database records in the API.
        
        Args:
            table (str): The table name
            pk (str): The primary key value (can be other than the traditional `id`)
            head (bool): Whether to include the body in the response
        '''
        return self._get(
            table = table, 
            query_args = request.args, 
            pk = pk,
            with_body = head
        )