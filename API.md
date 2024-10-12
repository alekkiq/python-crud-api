# API Documentation

## Headers
Requests to the API must include the following headers:

- ```X-API-KEY```: Your valid API key
- ```X-API-SECRET```: Your valid secret for the corresponding key

## Query parameters

### GET
Accepted query parameters for **GET** endpoints:

- `where`: Filter conditions for the query (e.g., `where=name='John'`).
- `order_by`: Column to order the results by (e.g., `order_by=name`).
- `sort`: Sort direction, either `asc` for ascending or `desc` for descending (e.g., `sort=asc`).
- `limit`: Maximum number of records to return (e.g., `limit=10`).
- `offset`: Number of records to skip before starting to return results (e.g., `offset=5`). The `limit` parameter must also be present for offset to work properly

### POST

### PUT

### DELETE

## Endpoints

### GET `/api/v1/<table>`
Retrieve all records from the specific table.

**Accepted Query Parameters:**
Refer to the [Query Parameters - GET](#query-parameters#get) section for details.

**Request:**
```bash
curl    -X GET "http://localhost:5000/api/v1/posts?where=title='My post'&order_by=name&sort=asc&limit=10&offset=5"
        -H "X-API-KEY: development_key"
        -H "X-API-SECRET: development_secret"
```

**Response:**
```json
# TODO
```

### GET `/api/v1/<table>/<id>`
Retrieve singular records from the specific table.

**Accepted Query Parameters:**
Refer to the [Query Parameters - GET](#query-parameters#get) section for details.

**Request:**
```bash
curl    -X GET "http://localhost:5000/api/v1/users/1"
        -H "X-API-KEY: development_key"
        -H "X-API-SECRET: development_secret"
```

**Response:**
```json
{
    "affected_rows": 1,
    "data": [
        {
            "created_at": "Fri, 11 Oct 2024 23:10:25 GMT",
            "email": "john@example.com",
            "id": 1,
            "name": "John Doe"
        }
    ],
    "query": {
        "arguments": {
            "where": "id = 1"
        },
        "statement": "SELECT * FROM `users` WHERE `id`='1'"
    },
    "result_group": true,
    "status": {
        "success": true,
        "type": "info"
    }
}
```

## POST
### TODO

## PUT
### TODO

## DELETE
### TODO