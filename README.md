# Python CRUD API

## Description
A Python-based CRUD (Create, Read, Update, Delete) API built with Flask and PyPika. This API provides endpoints to interact with an SQL database, supporting various operations on different tables. The project includes features like API key authentication, CORS support, and environment-based configuration.

## Features
- Support for MySQL(MariaDB), PostgreSQL and SQLite
- CRUD operations for database tables
- API key and secret authentication
- CORS support with configurable allowed origins
- Hiding certain tables from the API from non-allowed origins
- Environment-based configuration using `.env` files
- Logging and error handling
- Easy configuration

## Requirements
- Python 3.x (preferrably 3.12 <= x)
- MySQL database
- `pip` for Python package management

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/python-crud-api.git
    cd python-crud-api
    ```

2. Create a virtual environment and activate it (optional, but highly recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv/Scripts/activate   # On windows
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on the provided `.env.example`:
    ```bash
    cp .env.example .env
    ```

5. Update the `.env` file with your configuration values.

## Configuration
The application uses environment variables for configuration. The `.env` file should contain the following variables:

### **NOTE**: Add your own values with the same format you see in the example!

```properties
# App settings
APP_NAME="APP_NAME"
APP_ENV="development"
APP_VERSION="1.0"
APP_DEBUG="true"

# API settings
API_URL="api_url"
API_CLIENT_ID="client_id"
API_CLIENT_SECRET="client_secret"
API_KEYS="valid,api,keys"
API_SECRETS="valid:secret,api:secret,keys:secret"
API_HIDDEN_TABLES="your,protected,tables"
API_ALLOWED_ORIGINS="your,allowed,origins"

# Database settings
# Adjust these values to match your database type's settings
DB_CONNECTION="db_type" # mysql | postgresql | sqlite
DB_DATABASE="your_db_name" # If you are using sqlite, this should be the path to your database file ending with .db
DB_HOST="your_db_host"
DB_PORT="your_db_port"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_AUTO_COMMIT="true"
DB_COLLATION="utf8mb4_unicode_ci"
DB_CHARSET="utf8"
```

## Running the API
1. Ensure your database is running and accessible

2. Make sure your `.env` configurations are correct

3. Run the flask application:
    ```bash
    python main.py
    ```

## Authentication
Requests to the API must include the following headers:

- `X-API-KEY`: A valid API key
- `X-API-SECRET`: A valid secret for the corresponding API key

## CORS Configuration
CORS is configured to allow requests from specified origins. Update the `API_ALLOWED_ORIGINS` variable in the `.env` file to include the allowed origins, like so:

```properties
API_ALLOWED_ORIGINS="origin_1,origin_2"
```

## Logging
The application includes logging for debugging and error tracking. Logs are output directly to the console, as well as in the `logs/` subdirectory as separate `.log` files.

## API Docs
For a more in-depth API documentation, please refer to the [API.md](API.md) file.

## License

[LICENSE](LICENSE)

## Developer's TODO list

- Support for other Database engines (Postgre, Mongo, etc.)
- Write ***tests*** 🙄
- Write API documentation