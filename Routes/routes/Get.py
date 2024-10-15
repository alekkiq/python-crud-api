# Python deps & external libraries
import flask
from flask import jsonify, request, g

# The abstract class for the routes
from .. import Route

# Imports for proper typing
from Logger import Logger
from Database import DatabaseManager

# Constants
from constants import VALID_QUERY_ARGS, HIDDEN_TABLES

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
    
    def _get(self, table: str, query_args: dict, pk: str = None):
        '''
        Common logic for handling GET requests.
        
        Args:
            table (str): The table name
            query_args (dict): The query arguments
            pk (str, optional): The primary key value. Defaults to None.
        '''
        if self._block_hidden_table(table):
            return self._block_hidden_table(table)
        
        query_args = self._parse_query_args(request, VALID_QUERY_ARGS['GET'], table)
        
        if pk is not None:
            primary_key = self.db_manager.primary_key(table, self.db_manager.db_type)
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
            query_args=query_args
        )
        
        return jsonify(result)
    
    def get_all(self, table: str):
        '''
        Handles the GET requests for ALL database records in the API.
        
        Args:
            table (str): The table name
        '''
        return self._get(
            table = table, 
            query_args = request.args
        )

    def get_one(self, table: str, pk: str):
        '''
        Handles the GET requests for database records in the API.
        
        Args:
            table (str): The table name
            pk (str): The primary key value (can be other than the traditional `id`)
        '''
        return self._get(
            table = table, 
            query_args = request.args, 
            pk = pk
        )