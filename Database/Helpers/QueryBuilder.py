# Python deps & external libraries
from pypika import Table, Field, Order, Criterion
from pypika.dialects import MySQLQuery as Query

class QueryBuilder:
    '''
    Helper class for building the database queries.
    '''
    @staticmethod
    def apply_clause(query: Query, clause: str, value: str, query_args: dict) -> Query:
        match clause:
            case 'where':
                return QueryBuilder._where_clause(query, value)
            case 'order_by':
                return QueryBuilder._order_by_clause(query, value, query_args.get('sort', 'asc'))
            case 'limit':
                return QueryBuilder._limit_clause(query, value)
            case 'offset':
                return QueryBuilder._offset_clause(query, value, limit=query_args.get('limit', 0))
            # ... other clauses if needed
            case _:
                # return the unmodified query if the clause is not recognized
                return query
    
    @staticmethod
    def _where_clause(query: Query, value: str) -> Query:
        conditions = value.split(' AND ')
        for condition in conditions:
            key, value = condition.split('=')
            key = key.strip()
            value = value.strip().strip("'")
            query = query.where(Field(key) == value)
        return query
    
    @staticmethod
    def _order_by_clause(query: Query, value: str, sort: str) -> Query:
        if sort and sort.lower() in ['asc', 'desc']:
            return query.orderby(value, order=Order(sort.upper()))
        return query.orderby(value)
    
    @staticmethod
    def _limit_clause(query: Query, value: str) -> Query:
        return query.limit(value)
    
    @staticmethod
    def _offset_clause(query: Query, value: str) -> Query:
        return query.offset(value)