# Python deps & external libraries
from abc import ABC
import flask
from flask import jsonify

# Imports for proper typing
from Database import DatabaseManager
from Logger import Logger

# Status codes
from status import DATABASE_STATUS_MESSAGES as DB_STATUS_MESSAGES
from status import API_STATUS_MESSAGES as API_STATUS_MESSAGES

# Constants
from constants import API_PROTECTED_TABLES

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
    
    def _block_hidden_table(self, table: str) -> bool:
        '''
        Checks if `table` is visible to the current request origin.
        
        Args:
            table (str): The table name
        '''
        return flask.g.table_visibility == 'hidden' and table in API_PROTECTED_TABLES
    
    def _check_table_exists(self, table: str) -> bool:
        '''
        Checks if the `table` exists in the database.
        
        Args:
            table (str): The table name
        
        Returns:
            bool: True if the table exists, False otherwise
        '''
        return table in self.db_manager.get_table_names()
    
    def _before_db_action(self, table: str, query_args: dict):
        '''
        Executes common actions before the database action.
        
        Args:
            table (str): The table name
            query_args (dict): The query arguments
        '''
        checks = [
            (self._block_hidden_table, API_STATUS_MESSAGES['origin_not_allowed']),
            (lambda t: not self._check_table_exists(t), DB_STATUS_MESSAGES['table_not_found'](table)),
            # ... more checks if needed
        ]
        
        errors = []
        
        for check, error_message in checks:
            if check(table):
                self.api_logger.error(error_message['message'])
                errors.append({'success': False, 'status': error_message})
        
        if errors:
            # Return the first found error
            e = errors[0]
            return jsonify(e), e['status']['code']
        
        # all good -> continue
        return
    
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
    
    def _parse_data(self, data: dict, table: str, method: str = 'POST', primary_key_value: str = None) -> dict:
        '''
        Parses and validates the incoming request's `data` against the `table`'s columns.
        
        Args:
            data (dict): The data to be validated
            table (str): The table name for validation
            method (str): The HTTP method (POST, PUT, PATCH)
            primary_key_value (Any): The primary key value for fetching the existing record (PUT, PATCH)
        
        Returns:
            dict: The parsed data or an error message
        '''
        # Check for invalid columns
        invalid_columns_check = self._check_invalid_columns(data, table)
        if not invalid_columns_check['success']:
            return invalid_columns_check
        
        # Check for required fields (POST only)
        if method == 'POST':
            required_fields_check = self._check_required_fields(data, table)
            if not required_fields_check['success']:
                return required_fields_check
        
        # Check for unique fields already in use
        unique_fields_check = self._check_unique_fields(data, table)
        if not unique_fields_check['success']:
            return unique_fields_check
        
        # Check if incoming data is the same as the existing record (PUT & PATCH only)
        if method in ['PUT', 'PATCH']:
            existing_record_check = self._fetch_existing_record(table, primary_key_value)
            if not existing_record_check['success']:
                return existing_record_check
            
            existing_data = existing_record_check['data']
            if self._compare_data(existing_data, data):
                warning_message = DB_STATUS_MESSAGES['nothing_to_update'](table, primary_key_value)
                return {'success': False, 'status': warning_message}
        
        return {'success': True, 'data': data}
    
    # ------------------------------
    # Parse data helpers
    # ------------------------------
    def _check_unique_fields(self, data: dict, table: str) -> dict:
        unique_columns = self.db_manager.get_column_names(table, unique_fields=True)
        for column in unique_columns:
            if column in data:
                query_args = {'where': f'{column} = {data[column]}'}
                result = self.db_manager.select(
                    table_name=table, 
                    fields=[column], 
                    query_args=query_args
                )
                
                if result.get('success') and len(result.get('data')) > 0:
                    error_message = DB_STATUS_MESSAGES['already_used'](column, table)
                    self.api_logger.error(error_message['message'])
                    return {'success': False, 'status': error_message}
        
        return {'success': True}
    
    def _check_required_fields(self, data: dict, table: str) -> dict:
        required_fields = self.db_manager.get_column_names(table, required_fields=True)
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            error_message = DB_STATUS_MESSAGES['insert_fail'](data, table, f'Request Data is missing required fields of `{table}`. Missing fields: `{", ".join(missing_fields)}`')
            self.api_logger.error(error_message['message'])
            return {'success': False, 'status': error_message}
        
        return {'success': True}
    
    def _check_invalid_columns(self, data: dict, table: str) -> dict:
        valid_columns = self.db_manager.get_column_names(table)
        invalid_columns = [col for col in data if col not in valid_columns]
        
        if invalid_columns:
            error_message = DB_STATUS_MESSAGES['invalid_fields'](invalid_columns, table, f'Columns do not exist in table. `{str(invalid_columns)}`')
            self.api_logger.error(error_message['message'])
            return {'success': False, 'status': error_message}
        
        return {'success': True}
    
    def _fetch_existing_record(self, table: str, primary_key_value: str) -> dict:
        primary_key = self.db_manager.primary_key(table)
    
        query_args = {'where': f'{primary_key} = {primary_key_value}'}
        result = self.db_manager.select(
            table_name=table,
            fields=['*'],
            query_args=query_args
        )
        
        if result.get('success') and len(result.get('data')) > 0:
            return {'success': True, 'data': result['data'][0]}
        else:
            return {'success': False, 'status': f'Record with `{primary_key} = {primary_key_value}` not found.'}
        
        
    def _compare_data(self, existing_data: dict, incoming_data: dict) -> bool:
        for key, value in incoming_data.items():
            if key in existing_data and existing_data[key] != value:
                return False
        return True