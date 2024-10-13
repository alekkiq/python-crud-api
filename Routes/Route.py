# Python deps & external libraries
from abc import ABC
import flask
from flask import jsonify

# Imports for proper typing
from Database.DatabaseManager import DatabaseManager
from Logger.Logger import Logger

# Constants
from constants import HIDDEN_TABLES

class Route(ABC):
    '''
    Abstract class for the API routes.
    
    Attributes:
        db_manager (DatabaseManager): The database manager
        logger (Logger): The logger instance
        path (str): The route path
        callback (callable): The callback function
        method (str): The HTTP method
    '''
    def __init__(self, db_manager: DatabaseManager, db_logger: Logger, api_logger: Logger, path: str, method: str):
        self.db_manager = db_manager
        self.db_logger = db_logger
        self.api_logger = api_logger
        self.path = path
        self.method = method
    
    def _block_hidden_table(self, table: str):
        '''
        Checks if the table is visible to the current request origin.
        
        Args:
            table (str): The table name
        '''
        if flask.g.table_visibility == 'hidden' and table in HIDDEN_TABLES:
            return jsonify({'error': 'Table permission denied.', 'status': 404}), 404
        return None
    
    def _parse_query_args(self, request: flask.Request, valid_args: list, table: str) -> dict:
        '''
        Parses the query arguments from the request.
        
        Args:
            request (flask.Request): The request object
            valid_args (list): The list of valid query parameters
            table (str): The queried table name for validation
        
        Returns:
            dict: The query arguments
        '''
        query_args = {}
        valid_args_set = set(valid_args)
        
        # Set the valid query parameters first
        for arg in valid_args:
            if arg in request.args:
                query_args[arg] = request.args.get(arg)
        
        # Get valid columns for the table
        valid_columns = self.db_manager.get_column_names(table, self.db_manager.db_type)
        
        # View all other args (not in valid_args) as parameters for where clauses.
        where_clauses = [
            f'{key}={value}' for key, value in request.args.items()
            if key not in query_args and key in valid_columns
        ]
        
        # log all invalid where clause keys (unsupported query arguments)
        invalid_keys = [
            key for key in request.args.keys()
            if key not in query_args and key not in valid_args_set and key not in valid_columns
        ]
        for key in invalid_keys:
            self.api_logger.warning(f'Invalid where clause key: `{key}`')
        
        if where_clauses:
            query_args['where'] = ' AND '.join(where_clauses)
        
        return query_args
    
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