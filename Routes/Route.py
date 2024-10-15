# Python deps & external libraries
from abc import ABC
import flask
from flask import jsonify

# Imports for proper typing
from Database import DatabaseManager
from Logger import Logger

# Status codes
from STATUS import DATABASE_STATUS_MESSAGES as DB_STATUS_MESSAGES
from STATUS import API_STATUS_MESSAGES as API_STATUS_MESSAGES

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
        Checks if `table` is visible to the current request origin.
        
        Args:
            table (str): The table name
        '''
        if flask.g.table_visibility == 'hidden' and table in HIDDEN_TABLES:
            return jsonify({'error': 'Request origin permission denied.', 'status': 404}), 404
        return None
    
    def _parse_query_args(self, request: flask.Request, valid_args: list, table: str) -> dict:
        '''
        Parses the query arguments from the `request`.
        
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
            error_message = API_STATUS_MESSAGES['invalid_query_arg'](key)
            self.api_logger.warning(error_message['message'])
        
        if where_clauses:
            query_args['where'] = ' AND '.join(where_clauses)
        
        return query_args
    
    def _parse_data(self, data: dict, table: str) -> dict:
        '''
        Parses and validates the incoming request's `data` against the `table`'s columns.
        
        Args:
            data (dict): The data to be validated
            table (str): The table name for validation
        
        Returns:
            dict: The parsed data or an error message
        '''
        valid_columns = self.db_manager.get_column_names(table, self.db_manager.db_type)
        
        # Check for invalid columns
        invalid_columns = [col for col in data if col not in valid_columns]
        if invalid_columns:
            error_message = DB_STATUS_MESSAGES['insert_fail'](data, table, f'Invalid columns in insert data: `{", ".join(invalid_columns)}`')
            self.api_logger.error(error_message['message'])
            return {'success': False, 'status': error_message}
        
        # Check for required fields
        required_fields = self.db_manager.get_column_names(table, self.db_manager.db_type, required_fields=True)
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            error_message = DB_STATUS_MESSAGES['insert_fail'](data, table, f'Request Data is missing required fields of `{table}`. Missing fields: `{", ".join(missing_fields)}`')
            self.api_logger.error(error_message['message'])
            return {'success': False, 'status': error_message}
        
        # Check for unique fields already in use
        unique_columns = self.db_manager.get_column_names(table, self.db_manager.db_type, unique_fields=True)
        for column in unique_columns:
            if column in data:
                query_args = {'where': f'{column} = {data[column]}'}
                result = self.db_manager.select(
                    table, 
                    fields=[column], 
                    query_args=query_args
                )
                
                if result['result_group'] and len(result['data']) > 0:
                    error_message = DB_STATUS_MESSAGES['already_used'](column, table)
                    self.api_logger.error(error_message['message'])
                    return {'success': False, 'status': error_message}
        
        return {'success': True, 'data': data}
    
    def _handle_query_exceptions(self, query_args: dict, rules: list):
        '''
        Handles exceptions in query arguments `query_args` based on provided `rules`.
        
        Args:
            query_args (dict): The query arguments
            rules (list): A list of rules to apply to the query arguments
        '''
        for rule in rules:
            if rule['condition'](query_args):
                rule['action'](query_args)