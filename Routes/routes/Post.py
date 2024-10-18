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
        if self._before_db_action(table, query_args):
            return self._before_db_action(table, query_args)
        
        query_args = self._parse_query_args(request, API_VALID_QUERY_ARGS['POST'], table)
        
        # Parse and validate the data
        parsed_data = self._parse_data(data, table, method = 'POST')
        
        if not parsed_data.get('success'):
            return jsonify(parsed_data)
        
        result = self.db_manager.insert(
            table_name = table,
            data = parsed_data.get('data'),
            query_args = query_args
        )

        return jsonify(result)

    def insert_one(self, table: str):
        '''
        Handles the POST requests for inserting data into the database.
        
        Args:
            table (str): The table name
        '''
        return self._insert(
            table = table, 
            query_args = request.args,
            data = request.get_json()
        )