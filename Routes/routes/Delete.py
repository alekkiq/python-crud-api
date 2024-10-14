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

class Delete(Route):
    '''
    Handles the DELETE requests for the API.
    
    Attributes:
        db_manager (DatabaseManager): The database manager
        path (str): The route path
        db_logger (Logger): The database logger instance
        api_logger (Logger): The API logger instance
    '''
    def __init__(self, db_manager: DatabaseManager, path: str, db_logger: Logger, api_logger: Logger):
        super().__init__(db_manager, db_logger, api_logger, path, 'DELETE')
        
    def _delete(self, table: str, query_args: dict):
        '''
        Common logic for handling DELETE requests.
        
        Args:
            table (str): The table name
            pk (str): The primary key value
        '''
        if self._block_hidden_table(table):
            return self._block_hidden_table(table)

        result = self.db_manager.delete(
            table_name = table, 
            query_args = query_args
        )
        
        return jsonify(result)
    
    def delete_one(self, table: str, pk: str):
        '''
        Deletes a single record from the table by the primary key value.
        
        Args:
            table (str): The table name
            pk (str): The primary key value
        '''
        return self._delete(
            table = table, 
            query_args = {
                # Only delete the record with the primary key for safety
                'where': f'{self.db_manager.primary_key(table, self.db_manager.db_type)} = {pk}'
            }
        )