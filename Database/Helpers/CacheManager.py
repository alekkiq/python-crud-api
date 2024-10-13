class CacheManager:
    '''
    Helper class for managing the Database cache values.
    '''
    @staticmethod
    def check_cache(table: str, cache: dict) -> bool:
        '''
        Checks if the `table` is in the `cache`
        
        Args:
            table (str): The table name
            cache (dict): The cache dictionary
        '''
        return table in cache