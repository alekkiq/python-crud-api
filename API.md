# API Documentation

## Headers
Requests to the API ***must*** include the following headers:

- `X-API-KEY`: Your valid API key
- `X-API-SECRET`: Your valid secret for the corresponding key

With other than **GET** methods you also have to include:

- `Content-type: application/json`
- JSON format data: `{"name": "John Doe", "email": "johndoe@email.com"}` 

## Query parameters

### Common usage
In order to use extra parameters in your requests (mainly get requests), include them in the request URL like so:
```bash
# Simple pagination
https://your_api_url.com/api/v1/my_table?limit=25&offset=2
```

In the following sections you will get to know the supported query parameters for each request method type.

### GET
Accepted query parameters for **GET** endpoints:

- `where`: Filter conditions for the query (e.g., `name='John'`).
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
curl    -X GET "http://localhost:5000/api/v1/posts
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

### TODO
```json
{
}
```

## POST
### TODO

## PUT
### TODO

## DELETE
### TODO