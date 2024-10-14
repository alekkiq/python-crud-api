# Python deps & external libraries
from pypika import Table, Field, Order, Criterion
from pypika.dialects import MySQLQuery as Query

# DB Helper classes
from .Helpers import MetadataRetriever, QueryBuilder, CacheManager

# Imports for proper typing
from . import Database
from Logger import Logger

# Status messages
from STATUS import DATABASE_STATUS_MESSAGES as STATUS_MESSAGES

# Constants
from constants import VALID_QUERY_ARGS

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
        self.__primary_key_cache = {}
        self.__table_columns_cache = {}
        
        # Database type
        self.db_type = database.config.get('type')
    
    # ------------------------------
    # Public methods
    # ------------------------------
    def primary_key(self, table: str, db_type: str) -> str:
        '''
        Get the primary key for the table
        
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
            if db_type == 'sqlite':
                primary_key = MetadataRetriever.get_primary_key_sqlite(self.__db, table)
            else:  # mysql, postgresql, mariadb
                primary_key = MetadataRetriever.get_primary_key_information_schema(self.__db, table)
            if primary_key:
                self.__primary_key_cache[table] = primary_key
                return primary_key
            else:
                raise ValueError(f'No primary key found for table {table}')
        except Exception as e:
            self.__logger.error(f'Error getting primary key for table {table}: {e}')
            return None
        
    def get_table_names(self, db_type: str) -> list:
        '''
        Get the list of table names from the database
        
        Returns:
            list: The list of table names
        '''
        try:
            if db_type == 'sqlite':
                tables = MetadataRetriever.get_table_names_sqlite(self.__db)
            else: # mysql, postgresql, mariadb
                tables = MetadataRetriever.get_table_names_information_schema(self.__db)
            return tables
        except Exception as e:
            self.__logger.error(STATUS_MESSAGES['query_fail']('Error getting table names', str(e))['message'])
            return []
        
    def get_column_names(self, table: str, db_type: str, required_fields: bool = False, unique_fields: bool = False) -> list:
        '''
        Get the valid columns for the table
        
        Args:
            table (str): The table name
            db_type (str): The database type
            required_fields (bool): Whether to fetch only required columns
        
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
            if db_type == 'sqlite':
                columns = MetadataRetriever.get_column_names_sqlite(self.__db, table, required_fields, unique_fields)
            else:  # mysql, postgresql, mariadb
                columns = MetadataRetriever.get_column_names_information_schema(self.__db, table, required_fields, unique_fields)
            
            if columns:
                self.__table_columns_cache[cache_key] = columns
                return columns
            else:
                raise ValueError(f'No columns found for table {table}')
        except Exception as e:
            self.__logger.error(STATUS_MESSAGES['query_fail'](f'Error getting columns for `{table}`', str(e))['message'])
            return []
       
    # ------------------------------
    # Database actions (public)
    # ------------------------------
    def select(self, table_name: str, fields: list = ['*'], query_args: dict = None) -> dict:
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
        table = Table(table_name)
        query = Query.from_(table).select(*fields) # SELECT * FROM table
        
        # Add the query clauses
        if query_args is not None:
            for key, value in query_args.items():
                query = QueryBuilder.apply_clause(query, key, value, query_args)
        
        # Get the sql string of the constructed query
        sql = query.get_sql()
        
        result = self.__db.query(
            query = sql, 
            table_name = table_name,
            cursor_settings = {'dictionary': True},
            query_arguments = query_args
        )
        
        return result
    
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
                success_message = STATUS_MESSAGES['insert_success'](result, table_name)
                self.__logger.info(success_message['message'])
                return {'success': True, 'status': success_message, 'affected_rows': affected_rows}
            else:
                no_rows_message = STATUS_MESSAGES['insert_fail'](query_args, table_name, f'Record with `{query_args["where"]}` not found')
                self.__logger.warning(no_rows_message['message'])
                return {'success': False, 'status': no_rows_message, 'affected_rows': affected_rows}
        except Exception as e:
            error_message = STATUS_MESSAGES['insert_fail'](table_name, e)
            self.__logger.error(error_message['message'])
            return {'success': False, 'status': error_message, 'affected_rows': affected_rows}
        
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
        query = Query.from_(table).update() # UPDATE table
        
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
                success_message = STATUS_MESSAGES['update_success'](query_args, table_name)
                self.__logger.info(success_message['message'])
                return {'success': True, 'status': success_message}
            else:
                no_rows_message = STATUS_MESSAGES['update_fail'](query_args, table_name, f'Record with `{query_args["where"]}` not found')
                self.__logger.warning(no_rows_message['message'])
                return {'success': False, 'status': no_rows_message}
        except Exception as e:
            error_message = STATUS_MESSAGES['update_fail'](table_name, e)
            self.__logger.error(error_message['message'])
            return {'success': False, 'status': str(error_message)}
        
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
                success_message = STATUS_MESSAGES['delete_success'](query_args['where'], table_name)
                self.__logger.info(success_message['message'])
                return {'success': True, 'message': success_message}
            else:
                no_rows_message = STATUS_MESSAGES['delete_fail'](query_args['where'], table_name, f'Record with `{query_args["where"]}` not found in `{table_name}`')
                self.__logger.warning(no_rows_message['message'])
                return {'success': False, 'status': no_rows_message}
        except Exception as e:
            error_message = STATUS_MESSAGES['delete_fail'](query_args['where'], table_name, str(e))
            self.__logger.error(error_message['message'])
            return {'success': False, 'error': str(error_message)}