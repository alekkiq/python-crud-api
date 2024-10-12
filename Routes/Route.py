from abc import ABC, abstractmethod
import flask
from flask import jsonify
from Database import DatabaseManager

class Route(ABC):
    '''
    Abstract class for the routes.
    
    Attributes:
        db (DatabaseManager): The database manager
        path (str): The route path
        callback (callable): The callback function
        method (str): The HTTP method
    '''
    def __init__(self, db: DatabaseManager, path: str, method: str):
        self.db = db
        self.path = path
        self.method = method
    
    def _block_hidden_table(self, table: str):
        '''
        Checks if the table is visible to the current request origin.
        
        Args:
            table (str): The table name
        '''
        if flask.g.table_visibility == 'hidden' and table in flask.current_app.config.get('hidden_tables', []):
            return jsonify({'error': 'Origin permission denied.', 'status': 404}), 404
        return None
    
    def _parse_query_args(self, request: flask.Request, valid_args: list) -> dict:
        '''
        Parses the query arguments from the request.
        
        Args:
            request (flask.Request): The request object
            valid_args (list): The list of valid query parameters
            
        Returns:
            dict: The query arguments
        '''
        query_args = {}
        for arg in valid_args:
            if arg in request.args:
                query_args[arg] = request.args.get(arg)
        
        # Parse additional query parameters for the where clause
        where_clauses = []
        for key, value in request.args.items():
            if key not in valid_args:
                where_clauses.append(f"{key}='{value}'")
        
        if where_clauses:
            query_args['where'] = ' AND '.join(where_clauses)
        
        return query_args