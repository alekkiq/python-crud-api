# Python deps & external libraries
from pypika import Table, Field, Order, Criterion
from pypika.dialects import MySQLQuery as Query

# DB Helper classes
from .Helpers import MetadataRetriever, QueryBuilder, CacheManager

# Imports for proper typing
from . import Database
from Logger import Logger

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
        
    def get_column_names(self, table: str, db_type: str) -> list:
        '''
        Get the valid columns for the table
        
        Args:
            table (str): The table name
            db_type (str): The database type
        
        Returns:
            list: The list of valid columns
        '''      
        # Check if the table columns are in cache  
        if CacheManager.check_cache(table, self.__table_columns_cache):
            return self.__table_columns_cache[table]
        
        try:
            if db_type == 'sqlite':
                columns = MetadataRetriever.get_column_names_sqlite(self.__db, table)
            else:  # mysql, postgresql, mariadb
                columns = MetadataRetriever.get_column_names_information_schema(self.__db, table)
            if columns:
                self.__table_columns_cache[table] = columns
                return columns
            else:
                raise ValueError(f'No columns found for table {table}')
        except Exception as e:
            self.__logger.error(f'Error getting columns for table {table}: {e}')
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
        
        # Create the query clauses
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
    
    # ...
    
    def delete(self, table_name: str, query_args: dict) -> dict:
        '''
        Database action: DELETE
        
        Args:
            table_name (str): The name of the table to query
            query_args (dict): The query arguments
        
        Returns:
            dict: The result of the DELETE query
        '''
        table = Table(table_name)
        query = Query.from_(table).delete() # DELETE FROM table
        
        # Create the query clauses (only WHERE in this case)
        for key, value in query_args.items():
            query = QueryBuilder.apply_clause(query, key, value, query_args)
        
        # Get the sql string of the constructed query
        sql = query.get_sql()
        
        print(sql)
        
        result = self.__db.query(
            query = sql, 
            table_name = table_name,
            cursor_settings = {'dictionary': True},
            query_arguments = query_args
        )
        
        return result