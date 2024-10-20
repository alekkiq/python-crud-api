# Python CRUD API

## Description
A Python-based CRUD (Create, Read, Update, Delete) API built with Flask and PyPika. This API provides endpoints to interact with an SQL database, supporting various operations on different tables. The project includes features like support for multiple SQL DBMS's, CORS support and environment-based configuration.

## Features
- Support for the most common SQL DBMS's: MySQL (uses the MariaDB-intended connector), PostgreSQL and SQLite
- CRUD operations for database tables
- API actions via the core four HTTP methods (GET, POST, PUT, DELETE)
- CORS support with configurable allowed origins
- Protecting (hiding) certain tables from the API from non-allowed origins
- Fast and easy environment-based configuration using a `.env` file.
- Entry level logging and proper error handling
- \- JSON as the data type in requests

## Requirements
- Python 3.12.x <= 
    >(Built in 3.12.5)
- SQL database in MySQL, PostgreSQL or SQLite
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

    # Unix based systems:
    source venv/bin/activate
    
    # Windows systems:
    venv/Scripts/activate
    ```

3. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a new `.env` file based on the provided `.env.example`:
    ```bash
    cp .env.example .env
    ```

5. Update the `.env` file with your proper configuration values.

## Configuration
The application uses environment variables for configuration. The `.env` file must contain the following variables (provided in `.env.example`):

### **NOTE**: Add your own values with the same format you see in the example!

```properties
# .env.example

# App settings
APP_NAME="APP_NAME"
APP_ENV="development"               # development | production
APP_VERSION="1.0"
APP_DEBUG="true"

# API settings
API_URL="api_url"
API_PORT="your_port"
API_CLIENT_ID="client_id"
API_CLIENT_SECRET="client_secret"
API_KEYS="valid,api,keys"
API_SECRETS="valid:secret,api:secret,keys:secret"
API_API_PROTECTED_TABLES="your,protected,tables"
API_API_ALLOWED_ORIGINS="your,allowed,origins"
API_STORAGE_URI=""                  # Add a redis URI here if you're using redis in production

# API call limits
API_LIMITS_PER_DAY="10000"
API_LIMITS_PER_HOUR="1000"
API_LIMITS_PER_MINUTE="60"

# Database settings
# Adjust these values to match your database type's settings
DB_CONNECTION="db_type"             # mysql | postgresql | sqlite
DB_DATABASE="your_db_name"          # For SQLite, this should be the path to your database file ending with .db
DB_HOST="your_db_host"
DB_PORT="your_db_port"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_CHARSET="utf8"
DB_COLLATION="utf8mb4_unicode_ci"   # Mainly for MySQL to support wider range of characters

# Waitress settings (only if your ENV is production)
WAITRESS_HOST="your_host"
WAITRESS_PORT="your_port"
WAITRESS_THREADS="thread_count"
```

## Running the API
1. Ensure your SQL database is running and accessible

2. Make sure your `.env` configurations are correct
    - **Development / Local instances**:
        - Set your `APP_ENV` environment value to `development`:
            ```properties
            APP_ENV="development"
            ```

        - Ensure other development-specific configurations are set in your `.env` file as needed.

    - **Production** ***(HIGHLY not recommended)***:
        > **IMPORTANT**: This application was originally **NOT** built for production use **AT ALL**. If however, despite this warning you find the program production-level amazing, continue to the following steps, ***WITH YOUR OWN RISK***.<br><br>
        > The possibility for a "production" env was built solely to display the developers own skill of creating a "multi-env" compatible application.
        - Set your `APP_ENV` environment value as `production`:
            ```properties
            APP_ENV="production"
            ```

        - Set the correct `waitress` configuration in your `.env` file:
            ```properties
            WAITRESS_HOST="your_host"
            WAITRESS_PORT="your_port"
            WAITRESS_THREADS="thread_count"
            ```

3. Start the API by running `index.py`:
    ```bash
    python index.py
    ```

## Authentication
Requests to the API must include the following headers:

- `X-API-KEY`: A valid API key
- `X-API-SECRET`: A valid secret for the corresponding API key

## CORS Configuration
CORS is configured to allow requests from specified origins. By default, this only affects the action requests, keeping the GET requests public to all origins. Update the `API_API_ALLOWED_ORIGINS` variable in the `.env` file to allow origins to make POST & PUT requests to the API.

```properties
API_API_ALLOWED_ORIGINS="origin_1,origin_2"
```

## Logging

The application includes basic logging for debugging and error tracking. Logs are output to the console and saved in the `logs/` directory as separate `.log` files.

### Log Files

- **App Logs**: `logs/app/app.log`
  - Contains general application-level logs, including startup events and other significant actions.

- **Database Logs**: `logs/db/db.log`
  - Logs all database exceptions.

- **API Logs**: `logs/api/api.log`
  - Captures general API actions, including request headers, query parameters, HTTP methods, and other relevant details.

### Waitress (production only) `logs/waitress/waitress.log`


## API Docs
For a more in-depth API documentation, please refer to the [API.md](API.md) file.

## License

[LICENSE](LICENSE)

## Developer's TODO list

### Musts
- Write ***tests*** 🙄
- Write API documentation
- Add a status code to all `jsonify` returns
- Support for limiting api requests via .env variables "LIMITER_..."

### In case of borderline boredom
- Add support for other data types than json

## Background
The idea for this project originates from my (the developer's, duh) need for a simple CRUD-API in one of my fullstack projects; the classic TODO app. I initially built an *awfully* structured, and all around bad API directly to that project. Later on during the project I realised that it would make way more sense to build an easily configurable and more importantly, **re-usable** API, that could be utilized on later projects as well.