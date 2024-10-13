DATABASE_STATUS_CODES = {
    'software_error': 0,
    'connection_fail': 1,
    'connection_success': 2,
    'database_exists': 3,
    'database_not_exists': 4,
    'not_found': 5,
    'insert_success': 6,
    'insert_fail': 7,
    'already_used': 8,
    'deletion_success': 9,
    'deletion_fail': 10,
    'update_success': 11,
    'update_fail': 12,
    'key_mismatch': 13
}

DATABASE_STATUS_MESSAGES = {
    'software_error': lambda error: {
        'message': 'An error occurred in our program.',
        'status': DATABASE_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    'connection_fail': lambda config, error: {
        'message': f'Failed to establish a connection to the database. Configurations: `{config}`:\n{error}',
        'status': DATABASE_STATUS_CODES['connection_fail'],
        'type': 'error'
    },
    'connection_success': lambda config, db_type: {
        'message': f'Successfully established a connection to the `{db_type}` database at `{config.get('host')}:{config.get('port')}`.',
        'status': DATABASE_STATUS_CODES['connection_success'],
        'type': 'info'
    },
    'database_exists': lambda database: {
        'message': f'The database `{database}` already exists.',
        'status': DATABASE_STATUS_CODES['database_exists'],
        'type': 'info'
    },
    'database_not_exists': lambda database: {
        'message': f'The database `{database}` does not exist.',
        'status': DATABASE_STATUS_CODES['database_not_exists'],
        'type': 'error'
    },
    'not_found': lambda record: {
        'message': f'The requested record `{record}` was not found.',
        'status': DATABASE_STATUS_CODES['not_found'],
        'type': 'error'
    },
    'insert_success': lambda record: {
        'message': f'The record `{record}` was successfully inserted.',
        'status': DATABASE_STATUS_CODES['insert_success'],
        'type': 'success'
    },
    'insert_fail': lambda record, error: {
        'message': f'Failed to insert the record `{record}`. Error: {error}',
        'status': DATABASE_STATUS_CODES['insert_fail'],
        'type': 'error'
    },
    'already_used': lambda record: {
        'message': f'The record `{record}` is already in use.',
        'status': DATABASE_STATUS_CODES['already_used'],
        'type': 'error'
    },
    'deletion_success': lambda record: {
        'message': f'The record `{record}` was successfully deleted.',
        'status': DATABASE_STATUS_CODES['deletion_success'],
        'type': 'success'
    },
    'deletion_fail': lambda record, error: {
        'message': f'Failed to delete the record `{record}`. Error: {error}',
        'status': DATABASE_STATUS_CODES['deletion_fail'],
        'type': 'error'
    },
    'update_success': lambda record: {
        'message': f'The record `{record}` was successfully updated.',
        'status': DATABASE_STATUS_CODES['update_success'],
        'type': 'success'
    },
    'update_fail': lambda record, error: {
        'message': f'Failed to update the record `{record}`. Error: {error}',
        'status': DATABASE_STATUS_CODES['update_fail'],
        'type': 'error'
    },
    'key_mismatch': lambda key: {
        'message': f'The key `{key}` does not match a database record.',
        'status': DATABASE_STATUS_CODES['key_mismatch'],
        'type': 'error'
    }
}