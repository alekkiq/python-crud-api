WAITRESS_STATUS_CODES = {
    'software_error': 0,
    # ...
}

WAITRESS_STATUS_MESSAGES = {
    'software_error': lambda error: {
        'message': 'An error occurred in our program.',
        'status': WAITRESS_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    # ...
}