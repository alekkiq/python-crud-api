from .Database import Database
from pypika import Table, Field, Order, Criterion
from pypika.dialects import MySQLQuery as Query

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
        valid_args = ['where', 'order_by', 'sort', 'limit', 'offset']
        
        for key, value in query_args.items():
            if key in valid_args:
                q = self._apply_clause(q, key, value, query_args)
        
        # Finalize the query and get the SQL
        sql = q.get_sql()
        
        result = self.__db.query(sql, cursor_settings = {'dictionary': True})
        
        return result
    
    