API_STATUS_CODES = {
    'software_error': 500,          # Internal Server Error
    'invalid_query_arg': 400,       # Bad Request
    # ...
}

API_STATUS_MESSAGES = {
    'software_error': lambda error: {
        'message': 'An error occurred in our program.',
        'status': API_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    'invalid_query_arg': lambda arg: {
        'message': f'Invalid query argument: `{arg}`',
        'status': API_STATUS_CODES['invalid_query_arg'],
        'type': 'warning'
    },
    # ...
}