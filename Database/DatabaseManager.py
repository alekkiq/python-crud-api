# Python deps & external libraries
from pypika import Table, Field, Order, Criterion
from pypika.dialects import MySQLQuery as Query

# DB Helper classes
from .Helpers import MetadataRetriever, QueryBuilder, CacheManager

# Imports for proper typing
from . import Database
from Logger import Logger

# Status messages
from status import DATABASE_STATUS_MESSAGES as STATUS_MESSAGES

# Constants
from constants import API_VALID_QUERY_ARGS

class DatabaseManager:
    '''
    DatabaseManager class is responsible for handling the database actions.
    
    Attributes:
        db (Database): The database instance
        logger (Logger): The logger instance
    '''
    def __init__(self, database: Database, logger: Logger):
        self.__logger = logger
        self.__db = database
        
        # Caches for common metadata
        self.__primary_key_cache = {}
        self.__table_columns_cache = {}
        self.__table_names_cache = []
        
        # Database type
        self.db_type = self.__db.db_type
    
    # ------------------------------
    # Public methods
    # ------------------------------
    def primary_key(self, table: str) -> str:
        '''
        Get the primary key for `table` from the active database.
        
        Args:
            table (str): The table name
            db_type (str): The database type
        
        Returns:
            str: The primary key field
        '''
        # Check if the primary key is in cache
        if CacheManager.check_cache(table, self.__primary_key_cache):
            return self.__primary_key_cache[table]
        
        try:
            primary_key = MetadataRetriever.get_primary_key(self.__db, table)
            
            if primary_key:
                self.__primary_key_cache[table] = primary_key
                return primary_key
            else:
                raise ValueError(f'No primary key found for table {table}')
        except Exception as e:
            self.__logger.error(f'Error getting primary key for table {table}: {e}')
            return None
        
    def get_table_names(self) -> list:
        '''
        Get the list of table names from the `db_type` database.
        
        Args:
            db_type (str): The database type
        
        Returns:
            list: The list of table names
        '''
        # Check if the table names are in cache
        if self.__table_names_cache:
            return self.__table_names_cache
        
        try:
            db_tables = MetadataRetriever.get_table_names(self.__db)
            
            if db_tables:
                self.__table_names_cache.extend(db_tables)
                return db_tables
        except Exception as e:
            self.__logger.error(STATUS_MESSAGES['query_fail']('Error getting table names', str(e))['message'])
            return []
        
    def get_column_names(self, table: str, required_fields: bool = False, unique_fields: bool = False) -> list:
        '''
        Gets valid columns for `table` from the `db_type` database.
        
        Args:
            table (str): The table name
            db_type (str): The database type
            required_fields (bool): Whether to fetch only required columns
            unique_fields (bool): Whether to fetch only unique columns
        
        Returns:
            list: The list of valid columns
        '''
        if required_fields:
            cache_key = f'{table}_required'
        elif unique_fields:
            cache_key = f'{table}_unique'
        else:
            cache_key = table
        
        # Check if the table columns are in cache  
        if CacheManager.check_cache(cache_key, self.__table_columns_cache):
            return self.__table_columns_cache[cache_key]
        
        try:
            columns = MetadataRetriever.get_column_names(self.__db, table, required_fields, unique_fields)
            
            if columns:
                self.__table_columns_cache[cache_key] = columns
                return columns
            else:
                raise ValueError(f'No columns found for table {table}')
        except Exception as e:
            self.__logger.error(STATUS_MESSAGES['query_fail'](f'Error getting columns for `{table}`', str(e))['message'])
            return []
        
    # ------------------------------
    # Helper methods
    # ------------------------------
    def _create_status_result(self, status_type: str, *args, **kwargs) -> dict:
        '''
        Create a status message for the query.
        
        Args:
            status_type (str): The type of status message (e.g., 'query_fail', 'insert_fail')
            *args: Positional arguments for the status message function
            **kwargs: Keyword arguments to show in the result
        
        Returns:
            dict: The status message
        '''
        status_message = STATUS_MESSAGES[status_type](*args, **kwargs)
        if status_message['type'] == 'error':
            self.__logger.error(status_message['message'])
            success = False
        elif status_message['type'] == 'warning':
            self.__logger.warning(status_message['message'])
            success = False
        else:
            self.__logger.info(status_message['message'])
            success = True
            
        return {
            'success': success,
            'status': status_message,
            **kwargs
        }
       
    # ------------------------------
    # Database actions (public)
    # ------------------------------
    def select(self, table_name: str, fields: list = ['*'], query_args: dict = None, with_fetch: bool = True) -> dict:
        '''
        Database action: SELECT
        
        Args:
            table_name (str): The name of the table to query
            fields (list): A list of fields to select
            id (optional): The record ID
            where (optional): Conditions for filtering the results
            order_by (optional): Field(s) to order the results by
            sort (optional): Sort order (ASC or DESC)
            limit (optional): Limit on the number of results
            offset (optional): Offset for pagination
        
        Returns:
            dict: The result of the SELECT query
        '''
        if table_name not in self.get_table_names():
            return self._create_status_result('table_not_found', table_name)
        
        # Hard coded defaults
        # -> helps handling larger database table selects
        # -> to select ALL records, use limit=-1
        DEFAULT_OFFSET = 0
        DEFAULT_LIMIT = 100
        
        table = Table(table_name)
        query = Query.from_(table).select(*fields) # SELECT * FROM table
        
        # Add the query clauses
        if query_args is not None:
            for key, value in query_args.items():
                query = QueryBuilder.apply_clause(query, key, value, query_args)
        
        # Apply the defaults
        limit = query_args.get('limit', DEFAULT_LIMIT)
        offset = query_args.get('offset', DEFAULT_OFFSET)
        query = query.limit(limit).offset(offset)
        
        # Get the sql string of the constructed query
        sql = query.get_sql()
        try:
            result = self.__db.query(
                query = sql, 
                table_name = table_name,
                cursor_settings = {'dictionary': True},
                query_arguments = query_args,
                with_body = with_fetch
            )
            
            if with_fetch and not result.get('result_group') and len(result.get('data')) == 0:
                return self._create_status_result('query_not_found', sql)
            
            return result
        except Exception as e:
            return self._create_status_result('query_fail', str(e), sql)
    
    def insert(self, table_name: str, data: dict, query_args: dict) -> dict:
        '''
        Database action: INSERT
        
        Args:
            table_name (str): The name of the table to query
            query_args (dict): The query arguments
        
        Returns:
            dict: The result of the INSERT query (as status json)
        '''
        table = Table(table_name)
        query = Query.into(table) # INSERT INTO table
        
        # Add the data to the query
        columns = [Field(key) for key in data.keys()]
        values = [value for value in data.values()]
        query = query.columns(*columns).insert(*values)
        
        # Get the SQL string of the constructed query
        sql = query.get_sql()
        
        try:
            result = self.__db.query(
                query = sql, 
                table_name = table_name,
                cursor_settings = {'dictionary': True},
                query_arguments = query_args
            )
            affected_rows = result.get('affected_rows', 0)
            
            if affected_rows > 0:
                return self._create_status_result('insert_success', table_name)
            else:
                return self._create_status_result('insert_fail', data, table_name, f'Failed to insert record into `{table_name}`')
        except Exception as e:
            return self._create_status_result('insert_fail', data, table_name, str(e))
        
    def update(self, table_name: str, data: dict, query_args: dict) -> dict:
        '''
        Database action: UPDATE
        
        Args:
            table_name (str): The name of the table to query
            data (dict): The data to update
            query_args (dict): The query arguments
        
        Returns:
            dict: The result of the UPDATE query (as status json)
        '''
        if query_args is None or 'where' not in query_args:
            return {'success': False, 'error': STATUS_MESSAGES['update_fail'](table_name, 'No WHERE clause provided.')}
        
        table = Table(table_name)
        query = Query.update(table) # UPDATE table
        
        # Add the data to the query
        for key, value in data.items():
            query = query.set(Field(key), value)
        
        # Add the query clauses
        for key, value in query_args.items():
            query = QueryBuilder.apply_clause(query, key, value, query_args)
            
        # Get the SQL string of the constructed query
        sql = query.get_sql()

        try:
            result = self.__db.query(
                query = sql, 
                table_name = table_name,
                cursor_settings = {'dictionary': True},
                query_arguments = query_args
            )
            affected_rows = result.get('affected_rows', 0)
            
            if affected_rows > 0:
                return self._create_status_result('update_success', query_args.get('where'), table_name)
            else:
                return self._create_status_result('update_fail', query_args.get('where'), table_name, f'Record with `{query_args["where"]}` not found')
        except Exception as e:
            return self._create_status_result('update_fail', query_args.get('where'), table_name, str(e))
        
    def delete(self, table_name: str, query_args: dict) -> dict:
        '''
        Database action: DELETE
        
        Args:
            table_name (str): The name of the table to query
            query_args (dict): The query arguments
        
        Returns:
            dict: The result of the DELETE query (as status json)
        '''
        table = Table(table_name)
        query = Query.from_(table).delete() # DELETE FROM table
        
        # Create the query clauses (only WHERE in this case)
        if query_args is not None:
            for key, value in query_args.items():
                query = QueryBuilder.apply_clause(query, key, value, query_args)
        
        # Get the sql string of the constructed query
        sql = query.get_sql()
    
        try:
            result = self.__db.query(
                query = sql, 
                table_name = table_name,
                cursor_settings = {'dictionary': True},
                query_arguments = query_args
            )
            affected_rows = result.get('affected_rows', 0)
            
            if affected_rows > 0:
                return self._create_status_result('delete_success', query_args['where'], table_name)
            else:
                return self._create_status_result('delete_fail', query_args['where'], table_name, f'Record with `{query_args["where"]}` not found in `{table_name}`')
        except Exception as e:
            return self._create_status_result('delete_fail', query_args['where'], table_name, str(e))