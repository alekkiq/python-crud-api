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

class Post(Route):
    '''
    Handles the GET requests for the API.
    
    Attributes:
        db_manager (DatabaseManager): The database manager
        path (str): The route path
        db_logger (Logger): The database logger instance
        api_logger (Logger): The API logger instance
    '''
    def __init__(self, db_manager: DatabaseManager, path: str, db_logger: Logger, api_logger: Logger):
        super().__init__(db_manager, db_logger, api_logger, path, 'POST')
        
    def _insert(self, table: str, query_args: dict, data: dict):
        '''
        Common logic for handling POST requests.
        
        Args:
            table (str): The table name
            query_args (dict): The query arguments
            data (dict): The data to be inserted
        '''
        if self._block_hidden_table(table):
            return self._block_hidden_table(table)
        
        # Parse and validate the data
        parsed_data = self._parse_data(data, table)
        if not parsed_data['success']:
            return jsonify(parsed_data)
        
        query_args = self._parse_query_args(request, VALID_QUERY_ARGS['POST'], table)
        
        result = self.db_manager.insert(
            table_name = table,
            data = parsed_data['data'],
            query_args = query_args
        )

        return jsonify(result)

    def insert_one(self, table: str):
        '''
        Handles the POST requests for inserting data into the database.
        
        Args:
            table (str): The table name
        '''
        if not request.get_json():
            return jsonify({'error': 'No data provided.', 'status': 400}), 400
        
        return self._insert(
            table = table, 
            query_args = request.args,
            data = request.get_json()
        )