# ----------------------------------------------------------------
# This file contains the utility functions for the REST API.
# ----------------------------------------------------------------

class ParseUtils:
    @staticmethod
    def parse_secrets(secrets_str: str, logger = None) -> dict:
        '''
        Parse the secrets string `secrets_str` into a dictionary.
        
        Args:
            secrets_str (str): The secrets string
            
        Returns:
            dict: The secrets dictionary
        '''
        secrets = {}
        
        has_errors = False
        
        for item in secrets_str.split(','):
            parts = item.split(':')
            if len(parts) == 2:
                key, secret = parts
                secrets[key] = secret
                has_errors = False
            else:
                has_errors = True
                
        if logger:
            if has_errors:
                logger.error('Error parsing the secrets string.')
            else:
                logger.info('Secrets parsed successfully.')
        else:
            if has_errors:
                print('Error parsing the secrets string.')
            else:
                print('Secrets parsed successfully.')
        
        return secrets