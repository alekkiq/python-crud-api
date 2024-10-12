DATABASE_STATUS_CODES = {
    'software_error': 0,
    'not_found': 1,
    'insert_success': 2,
    'insert_fail': 3,
    'already_used': 4,
    'deletion_success': 5,
    'deletion_fail': 6,
    'update_success': 7,
    'update_fail': 8,
    'key_mismatch': 9,
    'database_exists': 10,
    'database_not_exists': 11,
    'connection_fail': 12,
    'connection_success': 13
}

DATABASE_STATUS_MESSAGES = {
    'software_error': lambda error: {
        'message': 'An error occurred in our program.',
        'status': DATABASE_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    'query_error': lambda error, query: {
        'message': f'An error occurred while executing the query `{query}`:\n{error}',
        'status': DATABASE_STATUS_CODES['software_error'],
        'error': error,
        'type': 'error'
    },
    'query_success': lambda query: {
        'message': f'Query `{query}` executed successfully.',
        'status': DATABASE_STATUS_CODES['software_error'],
        'type': 'info'
    },
    'not_found': lambda id, table: {
        'message': f'Record with the id `{id}` was not found in `{table}`.',
        'status': DATABASE_STATUS_CODES['not_found'],
        'type': 'error'
    },
    'insert_success': lambda id, table: {
        'message': f'Successfully inserted record with id `{id}` to `{table}`.',
        'status': DATABASE_STATUS_CODES['insert_success'],
        'type': 'info'
    },
    'insert_fail': lambda id, table: {
        'message': f'Record not added. Id `{id}` is empty or invalid at `{table}`.',
        'status': DATABASE_STATUS_CODES['insert_fail'],
        'type': 'fail'
    },
    'already_used': lambda field, value, table: {
        'message': f'The {field} `{value}` is already used in `{table}`.',
        'status': DATABASE_STATUS_CODES['already_used'],
        'type': 'error',
        'field': field,
        'value': value
    },
    'deletion_success': lambda id, table: {
        'message': f'Successfully deleted record with id `{id}` from `{table}`.',
        'status': DATABASE_STATUS_CODES['deletion_success'],
        'type': 'info'
    },
    'deletion_fail': lambda id, table: {
        'message': f'Failed to delete record with id `{id}` from `{table}`.',
        'status': DATABASE_STATUS_CODES['deletion_fail'],
        'type': 'fail'
    },
    'update_success': lambda id, table: {
        'message': f'Successfully updated record with id `{id}` in `{table}`.',
        'status': DATABASE_STATUS_CODES['update_success'],
        'type': 'info'
    },
    'update_fail': lambda id, table: {
        'message': f'Failed to update record with id `{id}` in `{table}`.',
        'status': DATABASE_STATUS_CODES['update_fail'],
        'type': 'fail'
    },
    'key_mismatch': lambda expected, received: {
        'message': f'Key mismatch error. Expected `{expected}`, but received `{received}`.',
        'status': DATABASE_STATUS_CODES['key_mismatch'],
        'type': 'error'
    },
    'connection_fail': lambda config, error: {
        'message': f'Failed to establish a connection to the database: `{config}`:\n{error}',
        'status': DATABASE_STATUS_CODES['connection_fail'],
        'type': 'error'
    },
    'connection_success': lambda config: {
        'message': f'Successfully established a connection to the database: `{config}`',
        'status': DATABASE_STATUS_CODES['connection_success'],
        'type': 'info'
    },
    'database_exists': lambda database: {
        'message': 'Database already exists.',
        'status': DATABASE_STATUS_CODES['database_exists'],
        'type': 'info'
    },
    'database_not_exists': lambda database: {
        'message': 'Database does not exist.',
        'status': DATABASE_STATUS_CODES['database_not_exists'],
        'type': 'error'
    }
}