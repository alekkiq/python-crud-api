# Python CRUD API

## Description
A Python-based CRUD (Create, Read, Update, Delete) API built with Flask and PyPika. This API provides endpoints to interact with an SQL database, supporting various operations on different tables. The project includes features like API key authentication, CORS support, and environment-based configuration.

## Features
- Support for the most common SQL engines: MySQL(MariaDB), PostgreSQL and SQLite
- CRUD operations for database tables
- API key and secret authentication
- CORS support with configurable allowed origins
- Hiding certain tables from the API from non-allowed origins
- Fast and easy environment-based configuration using a `.env` file. 
- Proper logging and error handling

## Requirements
- Python 3.12.x or newer (built with 3.12.5)
- SQL database in MySQL(MariaDB), PostgreSQL or SQLite
- `pip` for Python package management

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/alekkiq/python-crud-api.git
    cd python-crud-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv/Scripts/activate   # On windows
    ```

3. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a new `.env` file based on the provided `.env.example`:
    ```bash
    cp .env.example .env
    ```

5. Update the `.env` file with your configuration values.

## Configuration
The application uses environment variables for configuration. The `.env` file should contain the following variables:

### **NOTE**: Add your own values with the same format you see in the example!

```properties
# .env.example

# App settings
APP_NAME="APP_NAME"
APP_ENV="development" # development | production
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

# Waitress settings (only if your ENV is production)
WAITRESS_HOST="your_host"
WAITRESS_PORT="your_port"
WAITRESS_THREADS="thread_count"
```

## Running the API
1. Ensure your SQL database is running and accessible

2. Make sure your `.env` configurations are correct
    - **Development / Local instances**:
        - Set your `APP_ENV` environment value to `development` or `local`:
            ```properties
            APP_ENV="development"
            ```

        - Ensure other development-specific configurations are set in your `.env` file as needed.

    - **Production** ***(HIGHLY not recommended)***:
        > **IMPORTANT**: This application was originally **NOT** built for production use **AT ALL**. If however, despite this warning you find the program production-level amazing, continue to the following steps, ***with your own risk***.<br><br>
        > The possibility for a "production" env was built solely to display the developers own skill of creating a "multi-env" application.
        - Set your `APP_ENV` environment value as `production`:
            ```properties
            APP_ENV="production"
            ```

        - Set the correct `waitress` configuration in your `.env` file:
            ```properties
            WAITRESS_HOST="0.0.0.0"
            WAITRESS_PORT="5000"
            WAITRESS_THREADS="4"
            ```

3. Start the API from `index.py`:
    ```bash
    python index.py
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
The application includes entry-level logging for debugging and error tracking. Logs are output directly to the console, as well as in the `logs/` folder as separate `.log` files.

### App `logs/app/app.log`
The general app-level logs, for example, the whole app startup gets logged here.

### Database `logs/db/db.log`
All database actions have basic level of logging. For example, each query executed in the database gets logged.

### API `logs/api/api.log`
The most general API actions haev basic logging as well. For example, the whole (but simplified) API call gets logged, logging stuff like the call's headers, query arguments, http method and other relevant values.

### Waitress (production only) `logs/waitress/waitress.log`


## API Docs
For a more in-depth API documentation, please refer to the [API.md](API.md) file.

## License

[LICENSE](LICENSE)

## Developer's TODO list

- Write ***tests*** 🙄
- Write API documentation

## Background
The idea for this project originates from my (the developer's, duh) need for a simple CRUD-API in one of my fullstack projects; the classic TODO app. I initially built an *awfully* structured, and all around bad API directly to that project. Later on during the project I realised that it would make way more sense to build an easily configurable and more importantly, **re-usable** API, that could be utilized on later projects as well.