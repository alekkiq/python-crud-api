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

class Put(Route):
    '''
    Handles the PUT requests for the API.
    
    Attributes:
        db_manager (DatabaseManager): The database manager
        path (str): The route path
        db_logger (Logger): The database logger instance
        api_logger (Logger): The API logger instance
    '''
    def __init__(self, db_manager: DatabaseManager, path: str, db_logger: Logger, api_logger: Logger):
        super().__init__(db_manager, db_logger, api_logger, path, 'PUT')
        
    def _update(self, table: str, query_args: dict, data: dict):
        '''
        Common logic for handling PUT requests.
        
        Args:
            table (str): The table name
            query_args (dict): The query arguments
            data (dict): The data to be updated
        '''
        if self._block_hidden_table(table):
            return self._block_hidden_table(table)
        
        # Parse and validate the data
        parsed_data = self._parse_data(data, table)
        if not parsed_data['success']:
            return jsonify(parsed_data)
        
        query_args = self._parse_query_args(request, VALID_QUERY_ARGS['PUT'], table)
        
        result = self.db_manager.update(
            table_name = table,
            data = parsed_data['data'],
            query_args = query_args
        )
        
        return jsonify(result)
        
    def update_one(self, table: str):
        '''
        Handles the PUT requests for updating data in the database.
        
        Args:
            table (str): The table name
        '''
        if not request.get_json():
            return jsonify({'error': 'No data provided.', 'status': 400}), 400
        
        return self._update(
            table = table, 
            query_args = request.args, 
            data = request.get_json()
        )