APP_STATUS_CODES = {
    'software_error': 500,          # Internal Server Error
    # ...
}

APP_STATUS_MESSAGES = {
    'software_error': lambda error: {
        'message': 'An error occurred in our program.',
        'status': APP_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    # ...
}