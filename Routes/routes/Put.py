# Python deps & external libraries
import flask
from flask import jsonify, request, g

# The abstract class for the routes
from .. import Route

# Imports for proper typing
from Logger import Logger
from Database import DatabaseManager

from status import API_STATUS_MESSAGES as STATUS_MESSAGES

# Constants
from constants import API_VALID_QUERY_ARGS, API_PROTECTED_TABLES

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
        
    def _update(self, table: str, query_args: dict, data: dict, pk: str = None):
        '''
        Common logic for handling PUT requests.
        
        Args:
            table (str): The table name
            query_args (dict): The query arguments
            data (dict): The data to be updated
        '''
        if self._before_db_action(table, query_args):
            return self._before_db_action(table, query_args)
        
        # Parse and validate the data
        parsed_data = self._parse_data(data, table, method = 'PUT', primary_key_value = pk)
        if not parsed_data['success']:
            return jsonify(parsed_data)
        
        result = self.db_manager.update(
            table_name = table,
            data = parsed_data['data'],
            query_args = query_args
        )
        
        return jsonify(result)
        
    def update_one(self, table: str, pk: str):
        '''
        Handles the PUT requests for updating data in the database.
        
        Args:
            table (str): The table name
            pk (str): The primary key value
        '''
        return self._update(
            table = table, 
            query_args = {
                # Only update the record with the primary key for safety
                'where': f'{self.db_manager.primary_key(table)} = {pk}'
            }, 
            data = request.get_json(),
            pk = pk
        )