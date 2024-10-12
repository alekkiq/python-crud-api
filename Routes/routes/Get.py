from Routes import Route
import flask
from flask import jsonify, request, g
from Database.Manager import DatabaseManager

class Get(Route):
    valid_query_args = ['where', 'order_by', 'sort', 'limit', 'offset']
    
    def __init__(self, db: DatabaseManager, path: str):
        super().__init__(db, path, 'GET')
       
    def select_all(self, table: str):
        '''
        Handles the GET requests for the API.
        
        Args:
            table (str): The table name
        '''
        if self._block_hidden_table(table):
            return self._block_hidden_table(table)
        
        result = self.db.select(table_name=table, fields=['*'], query_args=self._parse_query_args(request, self.valid_query_args))
        
        return jsonify(result)
    
    def select_one(self, table: str, id: str):
        '''
        Handles the GET requests for the API.
        
        Args:
            table (str): The table name
            id (str): The record ID
        '''
        if self._block_hidden_table(table):
            return self._block_hidden_table(table)
        
        query_args = self._parse_query_args(request, self.valid_query_args)
        
        if id is not None:
            query_args['where'] = f"id = {id}"
        
        result = self.db.select(table_name=table, fields=['*'], query_args=query_args)
        
        return jsonify(result)