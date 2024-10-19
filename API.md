# API Documentation

## Headers
Requests to the API ***must*** include the following headers:

- `X-API-KEY`: Your valid API key
- `X-API-SECRET`: Your valid secret for the corresponding key

With data-involving methods (POST, PATCH, PUT) you also have to include:

- `Content-type: application/json`: Content type JSON
- `{"name": "John Doe", "email": "johndoe@email.com"}`: JSON format data

## Query parameters

### Common usage
In order to use extra parameters in your requests (mainly get requests), include them in the request URL like so:
```bash
# Simple pagination
https://your_api_url.com/api/v1/my_table?limit=25&offset=2
```

In the following sections you will get to know the supported query parameters for each request method type.

### GET / HEAD
Accepted query parameters for **GET** endpoints:

- `where`: Filter conditions for the query (e.g., `name='John'`).
- `order_by`: Column to order the results by (e.g., `order_by=name`).
- `sort`: Sort direction, either `asc` for ascending or `desc` for descending (e.g., `sort=asc`).
- `limit`: Maximum number of records to return (e.g., `limit=10`).
- `offset`: Number of records to skip before starting to return results (e.g., `offset=5`). The `limit` parameter must also be present for offset to work properly

### POST

No additional query parameters supported.

### PUT / PATCH

No additional query parameters supported. Updating a record happens via the primary key value from the URL.

### DELETE

No additional query parameters supported. Deleting a record happens via the primary key value from the URL.

## Endpoints

### GET `/api/v1/<table>`
Retrieve all records from the specific table.

**Accepted Query Parameters:**
Refer to the [Query Parameters - GET](#query-parameters#get) section for details.

**Request:**
```bash
curl    -X GET "http://localhost:5000/api/v1/authors
        -H "X-API-KEY: a_valid_key"
        -H "X-API-SECRET: a_valid_secret_for_key"
```

**Response:**
```json
{
  "affected_rows": 3,
  "data": [
    {
      "created_at": "Fri, 18 Oct 2024 17:56:23 GMT",
      "email": "john@example.com",
      "id": 1,
      "name": "John Doe"
    },
    {
      "created_at": "Fri, 18 Oct 2024 17:56:23 GMT",
      "email": "mary@example.com",
      "id": 2,
      "name": "Mary Jane"
    },
    {
      "created_at": "Fri, 18 Oct 2024 17:56:23 GMT",
      "email": "alice@example.com",
      "id": 3,
      "name": "Alice Johnson"
    }
  ],
  "links": {
    "next": null,
    "prev": null,
    "self": "/api/v1/authors"
  },
  "meta": {
    "page": 1,
    "per_page": 3,
    "total_pages": 1,
    "total_records": 3
  },
  "query": {
    "arguments": {},
    "sql": {
      "statement": "SELECT * FROM `authors` LIMIT 100",
      "type": "select"
    }
  },
  "result_group": true,
  "status": {
    "success": true,
    "type": "info"
  },
  "success": true,
  "timestamp": {
    "utc": "2024-10-19T20:51:37.063806+00:00"
  }
}
```

### GET `/api/v1/<table>/<id>`
Retrieve singular records from the specific table.

**Accepted Query Parameters:**
Refer to the [Query Parameters - GET](#query-parameters-get-head) section for details.

**Request:**
```bash
curl    -X GET "http://localhost:5000/api/v1/authors/1
        -H "X-API-KEY: a_valid_key"
        -H "X-API-SECRET: a_valid_secret_for_key"
```

**Response:**
```json
{
  "affected_rows": 1,
  "data": [
    {
      "created_at": "Fri, 18 Oct 2024 17:56:23 GMT",
      "email": "john@example.com",
      "id": 1,
      "name": "John Doe"
    }
  ],
  "links": {
    "next": null,
    "prev": null,
    "self": "/api/v1/authors"
  },
  "meta": {
    "page": 1,
    "per_page": 1,
    "total_pages": 1,
    "total_records": 1
  },
  "query": {
    "arguments": {
      "where": "id = 1"
    },
    "sql": {
      "statement": "SELECT * FROM `authors` WHERE `id`='1' LIMIT 100",
      "type": "select"
    }
  },
  "result_group": true,
  "status": {
    "success": true,
    "type": "info"
  },
  "success": true,
  "timestamp": {
    "utc": "2024-10-19T20:53:49.231520+00:00"
  }
}
```

## POST

Insert a new record to the specified database table.

**Accepted Query Parameters:**
Refer to the [Query Parameters - POST](#query-parameters-post) section for details.

**Request:**
```bash
curl    -X POST "http://localhost:5000/api/v1/authors
        -H "X-API-KEY: a_valid_key"
        -H "X-API-SECRET: a_valid_secret_for_key"
        -d '{"name": "Jane", "email": "jane@example.com"}'
        -H "Content-type: application/json"
```

**Response:**
```json
{
  "status": {
    "code": 201,
    "message": "Succesfully inserted a new record to `authors`",
    "type": "success"
  },
  "success": true
}
```

## PUT

Update an existing record specified with the primary key value in the specified table.

PUT should be used when updating all the record's fields.

**Accepted Query Parameters:**
Refer to the [Query Parameters - PUT / PATCH](#query-parameters-put-patch) section for details.

**Request:**
```bash
curl    -X PUT "http://localhost:5000/api/v1/authors/1
        -H "X-API-KEY: a_valid_key"
        -H "X-API-SECRET: a_valid_secret_for_key"
        -d '{"name": "Johnny", "email": "johnny@email.com"}'
        -H "Content-type: application/json"
```

**Response:**
```json
{
  "status": {
    "code": 200,
    "message": "Successfully updated record `id = 1` in `authors`",
    "type": "success"
  },
  "success": true
}
```

## PATCH

Update an existing record specified with the primary key value in the specified table.

PATCH should be used when only partially updating a record.

**Accepted Query Parameters:**
Refer to the [Query Parameters - PUT / PATCH](#query-parameters-put-patch) section for details.

**Request:**
```bash
curl    -X PATCH "http://localhost:5000/api/v1/authors/1
        -H "X-API-KEY: a_valid_key"
        -H "X-API-SECRET: a_valid_secret_for_key"
        -d '{"name": "Johnny"}'
        -H "Content-type: application/json"
```

**Response:**
```json
{
  "status": {
    "code": 200,
    "message": "Successfully updated record `id = 1` in `authors`",
    "type": "success"
  },
  "success": true
}
```

## DELETE

Delete an existing record specified with the primary key value in the specified table.

**Accepted Query Parameters:**
Refer to the [Query Parameters - DELETE](#query-parameters-put-patch) section for details.

**Request:**
```bash
curl    -X DELETE "http://localhost:5000/api/v1/authors/1
        -H "X-API-KEY: a_valid_key"
        -H "X-API-SECRET: a_valid_secret_for_key"
```

**Response:**
```json
{
  "status": {
    "code": 200,
    "message": "Successfully deleted `id = 1` from `authors`",
    "type": "success"
  },
  "success": true
}
```