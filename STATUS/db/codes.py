DATABASE_STATUS_CODES = {
    'software_error': 500,          # Internal Server Error
    'connection_fail': 503,         # Service Unavailable
    'connection_success': 200,      # OK
    'database_exists': 409,         # Conflict
    'database_not_exists': 404,     # Not Found
    'not_found': 404,               # Not Found
    'insert_success': 201,          # Created
    'insert_fail': 400,             # Bad Request
    'already_used': 409,            # Conflict
    'delete_success': 200,          # OK
    'delete_fail': 404,             # Not Found
    'update_success': 200,          # OK
    'update_fail': 400,             # Bad Request
    'key_mismatch': 400,            # Bad Request
    'query_fail': 400,              # Bad Request
    'query_success': 200            # OK
}

DATABASE_STATUS_MESSAGES = {
    'software_error': lambda error: {
        'message': 'An error occurred in our program',
        'status': DATABASE_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    'connection_fail': lambda config, error: {
        'message': f'Failed to establish a connection to the database. Configurations: `{config}`',
        'status': DATABASE_STATUS_CODES['connection_fail'],
        'error': error,
        'type': 'error',
    },
    'connection_success': lambda config, db_type: {
        'message': f'Successfully established a connection to the `{db_type}` database at `{config.get('host')}:{config.get('port')}`',
        'status': DATABASE_STATUS_CODES['connection_success'],
        'type': 'success'
    },
    'database_exists': lambda database: {
        'message': f'Database `{database}` already exists',
        'status': DATABASE_STATUS_CODES['database_exists'],
        'type': 'info'
    },
    'database_not_exists': lambda database: {
        'message': f'Database `{database}` does not exist',
        'status': DATABASE_STATUS_CODES['database_not_exists'],
        'type': 'error'
    },
    'not_found': lambda record: {
        'message': f'Requested record `{record}` was not found',
        'status': DATABASE_STATUS_CODES['not_found'],
        'type': 'error'
    },
    'query_fail': lambda error, query = None: {
        'message': f'Failed to execute query `{query}`',
        'status': DATABASE_STATUS_CODES['query_fail'],
        'error': error,
        'type': 'error'
    },
    'query_success': lambda query: {
        'message': f'Successfully executed query `{query}`',
        'status': DATABASE_STATUS_CODES['query_success'],
        'type': 'info'
    },
    'insert_success': lambda record, table: {
        'message': f'Succesfully inserted a new record to `{table}`',
        'status': DATABASE_STATUS_CODES['insert_success'],
        'type': 'success'
    },
    'insert_fail': lambda record, table, error: {
        'message': f'Failed inserting `{record}` to `{table}`',
        'status': DATABASE_STATUS_CODES['insert_fail'],
        'error': error,
        'type': 'error'
    },
    'already_used': lambda key, table: {
        'message': f'Unique key `{key}` is already in use in `{table}`',
        'status': DATABASE_STATUS_CODES['already_used'],
        'type': 'error'
    },
    'delete_success': lambda record, table: {
        'message': f'Successfully deleted `{record}` from `{table}`',
        'status': DATABASE_STATUS_CODES['delete_success'],
        'type': 'success'
    },
    'delete_fail': lambda record, table, error: {
        'message': f'Failed to delete the record `{record}` from `{table}`',
        'status': DATABASE_STATUS_CODES['delete_fail'],
        'error': error,
        'type': 'error'
    },
    'update_success': lambda record, table = None: {
        'message': f'Successfully updated record `{record}` in `{table}`',
        'status': DATABASE_STATUS_CODES['update_success'],
        'type': 'success'
    },
    'update_fail': lambda record, table, error: {
        'message': f'Failed to update the record `{record}` in `{table}`',
        'status': DATABASE_STATUS_CODES['update_fail'],
        'error': error,
        'type': 'error'
    },
    'key_mismatch': lambda key, table: {
        'message': f'Key `{key}` does not match a record in `{table}`.',
        'status': DATABASE_STATUS_CODES['key_mismatch'],
        'type': 'error'
    }
}