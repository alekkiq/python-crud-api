from .Database import Database

from pypika import Table, Field, Order, Criterion
from pypika.dialects import MySQLQuery as Query

from constants import VALID_QUERY_ARGS

class DatabaseManager:
    '''
    DatabaseManager class is responsible for handling the database actions.
    
    Attributes:
        db (Database): The database instance
        logger (Logger): The logger instance
    '''
    def __init__(self, database: Database, logger):
        self.__logger = logger
        self.__db = database
        self.__primary_key_cache = {}
        self.__table_columns_cache = {}
        
        # Database type
        self.db_type = database.config.get('type')
    
    # ------------------------------
    # Internal methods
    # ------------------------------
    def __check_cache(self, table: str, cache: dict) -> bool:
        '''
        Checks if the `table` is in the `cache`
        
        Args:
            table (str): The table name
            cache (dict): The cache dictionary
        '''
        return table in cache
    
    def __get_primary_key_sqlite(self, table: str) -> str:
        '''
        Gets the primary key for the table in SQLite
        
        Args:
            table (str): The table name
        
        Returns:
            str: The primary key field
        '''
        query = f'PRAGMA table_info({table})'
        result = self.__db.query(query)
        for row in result['data']:
            if row[5] == 1:  # Sixth column in the result set indicates if the column is a primary key
                return row[1]  # Second column in the result set contains the column names
        return None

    def __get_primary_key_information_schema(self, table: str) -> str:
        '''
        Gets the primary key for the table in MySQL, MariaDB, and PostgreSQL using SQL's native INFORMATION_SCHEMA
        
        Args:
            table (str): The table name
        
        Returns:
            str: The primary key field
        '''
        query = f'''
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = "{table}" AND COLUMN_KEY = "PRI"
        '''
        result = self.__db.query(query, cursor_settings={'dictionary': True})
        if result:
            return result['data'][0]['COLUMN_NAME']
        return None
    
    def _apply_clause(self, query: Query, clause: str, value: str, query_args: dict) -> Query:
        match clause:
            case 'where':
                return self._where_clause(query, value)
            case 'order_by':
                return self._order_by_clause(query, value, query_args.get('sort', 'asc'))
            case 'limit':
                return self._limit_clause(query, value)
            case 'offset':
                return self._offset_clause(query, value, limit = query_args.get('limit', 0))
            # ... other cases if needed
            case _:
                return query
    
    def _where_clause(self, query: Query, value: str) -> Query:
        conditions = value.split(' AND ')
        for condition in conditions:
            key, value = condition.split('=')
            key = key.strip()
            value = value.strip().strip("'")
            query = query.where(Field(key) == value)
        return query
    
    def _order_by_clause(self, query: Query, value: str, sort: str) -> Query:
        if sort and sort.lower() in ['asc', 'desc']:
            return query.orderby(value, order=Order(sort.upper()))
        return query.orderby(value)
    
    def _limit_clause(self, query: Query, value: str) -> Query:
        return query.limit(value)
    
    def _offset_clause(self, query: Query, value: str, limit: int = 0) -> Query:
        return query.offset(value)
    
    
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
        if self.__check_cache(table, self.__primary_key_cache):
            return self.__primary_key_cache[table]
        
        try:
            if db_type == 'sqlite':
                primary_key = self.__get_primary_key_sqlite(table)
            else:  # mysql, postgresql, mariadb
                primary_key = self.__get_primary_key_information_schema(table)
            
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
        if self.__check_cache(table, self.__table_columns_cache):
            return self.__table_columns_cache[table]
        
        try:
            if db_type == 'sqlite':
                columns = self.__get_column_names_sqlite(table)
            else:  # mysql, postgresql, mariadb
                columns = self.__get_column_names_information_schema(table)
            
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
        q = Query.from_(table).select(*fields) # SELECT * FROM table
        
        # Create the other query clauses
        valid_args = VALID_QUERY_ARGS['GET']
        
        for key, value in query_args.items():
            if key in valid_args:
                q = self._apply_clause(q, key, value, query_args)
        
        # Finalize the query and get the SQL
        sql = q.get_sql()
        
        result = self.__db.query(
            query = sql, 
            cursor_settings = {'dictionary': True},
            query_arguments = query_args
        )
        
        return result