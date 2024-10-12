DATABASE_STATUS_CODES = {
    "software_error": 0,
    "not_found": 1,
    "insert_success": 2,
    "insert_fail": 3,
    "already_used": 4,
    "deletion_success": 5,
    "deletion_fail": 6,
    "update_success": 7,
    "update_fail": 8,
    "key_mismatch": 9,
    "setup_success": 13,
    "setup_fail": 14,
    "database_exists": 15,
    "database_not_exists": 16
}

DATABASE_STATUS_MESSAGES = {
    "software_error": lambda error: {
        "message": "An error occurred in our program.",
        "status": DATABASE_STATUS_CODES["software_error"],
        "error": error,
        "type": "error"
    },
    "not_found": lambda id, table: {
        "message": f"Record with the id `{id}` was not found in `{table}`.",
        "status": DATABASE_STATUS_CODES["not_found"],
        "type": "error"
    },
    "insert_success": lambda id, table: {
        "message": f"Successfully inserted record with id `{id}` to `{table}`.",
        "status": DATABASE_STATUS_CODES["insert_success"],
        "type": "info"
    },
    "insert_fail": lambda id, table: {
        "message": f"Record not added. Id `{id}` is empty or invalid at `{table}`.",
        "status": DATABASE_STATUS_CODES["insert_fail"],
        "type": "fail"
    },
    "already_used": lambda field, value, table: {
        "message": f"The {field} `{value}` is already used in `{table}`.",
        "status": DATABASE_STATUS_CODES["already_used"],
        "type": "error",
        "field": field,
        "value": value
    },
    "deletion_success": lambda id, table: {
        "message": f"Successfully deleted record with id `{id}` from `{table}`.",
        "status": DATABASE_STATUS_CODES["deletion_success"],
        "type": "info"
    },
    "deletion_fail": lambda id, table: {
        "message": f"Failed to delete record with id `{id}` from `{table}`.",
        "status": DATABASE_STATUS_CODES["deletion_fail"],
        "type": "fail"
    },
    "update_success": lambda id, table: {
        "message": f"Successfully updated record with id `{id}` in `{table}`.",
        "status": DATABASE_STATUS_CODES["update_success"],
        "type": "info"
    },
    "update_fail": lambda id, table: {
        "message": f"Failed to update record with id `{id}` in `{table}`.",
        "status": DATABASE_STATUS_CODES["update_fail"],
        "type": "fail"
    },
    "key_mismatch": lambda expected, received: {
        "message": f"Key mismatch error. Expected `{expected}`, but received `{received}`.",
        "status": DATABASE_STATUS_CODES["key_mismatch"],
        "type": "error"
    },
    "setup_success": lambda: {
        "message": "Setup successful.",
        "status": DATABASE_STATUS_CODES["setup_success"],
        "type": "info"
    },
    "setup_fail": lambda error: {
        "message": f"Setup failed! {error}",
        "status": DATABASE_STATUS_CODES["setup_fail"],
        "type": "error"
    },
    "database_exists": lambda: {
        "message": "Database already exists.",
        "status": DATABASE_STATUS_CODES["database_exists"],
        "type": "info"
    },
    "database_not_exists": lambda: {
        "message": "Database does not exist.",
        "status": DATABASE_STATUS_CODES["database_not_exists"],
        "type": "error"
    }
}