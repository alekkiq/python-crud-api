# Python deps & external libraries
from abc import ABC
import flask
from flask import jsonify

# Constants
from constants import DatabaseManager, Logger, HIDDEN_TABLES

class Route(ABC):
    '''
    Abstract class for the API routes.
    
    Attributes:
        db (DatabaseManager): The database manager
        logger (Logger): The logger instance
        path (str): The route path
        callback (callable): The callback function
        method (str): The HTTP method
    '''
    def __init__(self, db: DatabaseManager, logger: Logger, path: str, method: str):
        self.db = db
        self.logger = logger
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
        for arg in valid_args:
            if arg in request.args:
                query_args[arg] = request.args.get(arg)
        
        # Get valid columns for the table
        valid_columns = self.db.get_valid_columns(table)
        
        # View all other query (not in valid_args) 
        # as parameters as where clauses.
        where_clauses = []
        for key, value in request.args.items():
            if key not in valid_args:
                if key in valid_columns:
                    where_clauses.append(f"{key}='{value}'")
                else:
                    self.logger.warning(f'Invalid where clause key: `{key}`')
        
        if where_clauses:
            query_args['where'] = ' AND '.join(where_clauses)
        
        return query_args