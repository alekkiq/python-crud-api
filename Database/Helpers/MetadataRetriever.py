# Imports for proper typing
from .. import Database

class MetadataRetriever:
    '''
    Helpers for retrieving metadata from a database
    '''
    @staticmethod
    def get_primary_key_sqlite(db: Database, table: str) -> str:
        '''
        Gets the primary key for the table in SQLite
        
        Args:
            table (str): The table name
        
        Returns:
            str: The primary key field
        '''
        query = f'PRAGMA table_info({table})'
        result = db.query(query, is_meta_query=True)
        for row in result['data']:
            if row[5] == 1:  # Sixth column in the result set indicates if the column is a primary key
                return row[1]  # Second column in the result set contains the column names
        return None

    @staticmethod
    def get_primary_key_information_schema(db: Database, table: str) -> str:
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
        result = db.query(query, cursor_settings={'dictionary': True}, is_meta_query=True)

        if result:
            primary_key_column = result['data'][0]['COLUMN_NAME']
            return primary_key_column
        return None
    
    @staticmethod
    def get_table_names_sqlite(db: Database) -> list:
        '''
        Retrieves the table names from MySQL, PostgreSQL, or MariaDB database.
        
        Args:
            db (Database): The database instance
            
        Returns:
            list: A list of table names
        '''
        query = '''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
        '''
        result = db.query(query, cursor_settings={'dictionary': True}, is_meta_query=True)

        if result:
            tables = [row['name'] for row in result['data']]
            return tables
        return []
    
    @staticmethod
    def get_table_names_information_schema(db: Database) -> list:
        '''
        Retrieves the table names from MySQL, PostgreSQL, or MariaDB database.
        
        Args:
            db (Database): The database instance
            
        Returns:
            list: A list of table names
        '''
        query = '''
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = "BASE TABLE"
        '''
        result = db.query(query, cursor_settings={'dictionary': True}, is_meta_query=True)

        if result:
            tables = [row['TABLE_NAME'] for row in result['data']]
            return tables
        return []

    @staticmethod
    def get_column_names_sqlite(db: Database, table: str, required_fields: bool = False, unique_fields: bool = False) -> list:
        '''
        Retrieves the column names for the specified table from an SQLite database.
        
        Args:
            db (Database): The database instance
            table (str): The name of the table
            required_fields (bool): If True, only return the required fields
            
        Returns:
            list: A list of column names
        '''
        
        # TODO - Add support for required & unique fields
        
        query = f'PRAGMA table_info({table})'
        result = db.query(query, is_meta_query=True)

        if result:
            columns = [row[1] for row in result['data']]
            return columns
        return []

    @staticmethod
    def get_column_names_information_schema(db: Database, table: str, required_fields: bool = False, unique_fields: bool = False) -> list:
        '''
        Retrieves the column names for the specified table from MySQL, PostgreSQL, or MariaDB database.
        
        Args:
            db (Database): The database instance
            table (str): The name of the table
            required_fields (bool): If True, only return the required fields
            
        Returns:
            list: A list of column names
        '''
        query = f'''
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = "{table}"
        '''
        
        if required_fields:
            query += ' AND IS_NULLABLE = "NO" AND COLUMN_DEFAULT IS NULL AND EXTRA NOT LIKE "%auto_increment%"'
        
        if unique_fields:
            query += ' AND COLUMN_KEY = "UNI"'
        
        result = db.query(query, cursor_settings={'dictionary': True}, is_meta_query=True)
        
        if result:
            columns = [row['COLUMN_NAME'] for row in result['data']]
            return columns
        return []