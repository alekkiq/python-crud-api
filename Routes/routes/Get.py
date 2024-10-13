# Python deps & external libraries
import flask
from flask import jsonify, request, g

# The abstract class for the routes
from Routes.Route import Route

# Internal modules
from Logger.Logger import Logger
from Database.Manager import DatabaseManager

# Constants
from constants import VALID_QUERY_ARGS, HIDDEN_TABLES

class Get(Route):
    '''
    Handles the GET requests for the API.
    
    Attributes:
        db (DatabaseManager): The database manager
        db_logger (Logger): The database logger instance
        api_logger (Logger): The API logger instance
        path (str): The route path
        method (str): The HTTP method
    '''
    def __init__(self, db: DatabaseManager, path: str, db_logger: Logger, api_logger: Logger):
        super().__init__(db, db_logger, api_logger, path, 'GET')
        
    def _handle_query_exceptions(self, query_args: dict, rules: list):
        '''
        Handles exceptions in query arguments based on provided rules.
        
        Args:
            query_args (dict): The query arguments
            rules (list): A list of rules to apply to the query arguments
        '''
        for rule in rules:
            if rule['condition'](query_args):
                rule['action'](query_args)
                
    def _offset_without_limit_condition(self, query_args: dict) -> bool:
        return 'offset' in query_args and 'limit' not in query_args

    def _remove_offset_action(self, query_args: dict):
        del query_args['offset']
       
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
            primary_key = self.db.primary_key(table)
            if primary_key is None:
                return jsonify({'error': 'Primary key not found'}), 400
            query_args['where'] = f'{primary_key} = {pk}'
        
        # Handle query exceptions
        rules = [
            {
                'condition': self._offset_without_limit_condition, 
                'action': self._remove_offset_action
            }
        ]
        self._handle_query_exceptions(query_args, rules)
        
        result = self.db.select(
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
            pk=pk
        )