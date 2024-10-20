API_STATUS_CODES = {
    'software_error': 500,          # Internal Server Error
    'bad_request': 400,             # Bad Request
    'not_found': 404,               # Not Found
    'too_many_requests': 429,       # Too Many Requests
    'origin_not_allowed': 405,      # Method/route Not Allowed
    'unauthorized': 403,            # Unauthorized
    'invalid_content_type': 400,    # Bad Request
    'invalid_method': 405,          # Method Not Allowed
    'invalid_query_arg': 400,       # Bad Request
    'no_data_provided': 400,        # Bad Request
    # ...
}

API_STATUS_MESSAGES = {
    'software_error': lambda error: {
        'message': 'An unexpected error occurred in our program.',
        'code': API_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    'not_found': lambda url, error: {
        'message': f'Resource not found at {url}',
        'code': API_STATUS_CODES['not_found'],
        'error': error,
        'type': 'error'
    },
    'bad_request': lambda error: {
        'message': 'Bad request. Check the request and try again.',
        'code': API_STATUS_CODES['bad_request'],
        'error': error,
        'type': 'error'
    },
    'unauthorized': {
        'message': 'Unauthorized. Please provide valid credentials.',
        'code': API_STATUS_CODES['unauthorized'],
        'type': 'error'
    },
    'too_many_requests': lambda error, allowed_rate: {
        'message': f'Too many requests. Please try again later. The allowed rate is {allowed_rate} requests per minute.',
        'code': API_STATUS_CODES['too_many_requests'],
        'error': error,
        'type': 'error'
    },
    'origin_not_allowed': {
        'message': f'Route not allowed for origin.',
        'code': API_STATUS_CODES['origin_not_allowed'],
        'type': 'error'
    },
    'invalid_method': lambda method, valid_methods, error = None: {
        'message': f'HTTP method `{method}` is not supported, or the request url is of invalid format. Valid methods are {", ".join(valid_methods)}',
        'code': API_STATUS_CODES['invalid_method'],
        'error': error,
        'type': 'error'
    },
    'invalid_content_type': lambda content_type, allowed_types: {
        'message': f'Content-type `{content_type}` is not supported. Use one of the following: {", ".join(allowed_types)}',
        'code': API_STATUS_CODES['invalid_content_type'],
        'type': 'error'
    },
    'no_content_type': {
        'message': 'Content-type header is required for this request.',
        'code': API_STATUS_CODES['invalid_content_type'],
        'type': 'error'
    },
    'invalid_query_arg': lambda arg, method, valid_args, error = None: {
        'message': f'Invalid query argument: `{arg}`. Valid arguments for `{method} are {", ".join(valid_args[method])}',
        'code': API_STATUS_CODES['invalid_query_arg'],
        'error': error,
        'type': 'warning'
    },
    'no_content_type': lambda content_types: {
        'message': f'Content-type header is required for this request. Use one of the following: {", ".join(content_types)}',
        'code': API_STATUS_CODES['invalid_content_type'],
        'type': 'error'
    },
    'no_data_provided': lambda data_types: {
        'message': f'Request must contain valid data. Use one of the following: {", ".join(data_types)}',
        'code': API_STATUS_CODES['no_data_provided'],
        'type': 'error'
    },
}