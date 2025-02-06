## Technology choices:

### Frontend: 

_streamlit_ - Streamlit is one of the framework  that a python programmer can use it with basic understanding how UI works.

### Backend:

Since this assignment contains multiple third-party API calls, the suitable choice will be to go with async programming
and use the co-routines to unblock and wait for the result, given that used the FastAPI as a backend

### Deployment
I have used docker-compose to deploy both frontend and backend, I'm using docker-compose here as number of service 
components are not many. Also, it can allow specifying dependency.

### What I have included
1. A bash script to build and run the frontend and backend
2. docker-compose.yaml which will build and start conainers
3. backend code 
4. frontend code

## API Documentation: URL Input Handler (GET)

### Overview

This API allows you to submit a URL as an input and get a response based on the content or processing associated with that URL.

### Endpoint
GET /api/scrape_reviews
### Query Parameters

The API accepts a URL as a query parameter.

| Parameter  | Type   | Description                                                     | Required |
|------------|--------|-----------------------------------------------------------------|----------|
| `url`      | string | The input URL is **limited to product reviews page** of the product | Yes      |

### Example Request
GET /api/scrape_reviews?url=https://www.amazon.in/OnePlus-28-85cm-11-35-inch-2-4K/product-reviews/B0CJ94J5CX/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews


### Response

The response depends on the implementation but typically will contain a status or result based on processing the provided URL.

#### Success Response (HTTP 200)

If the URL is valid and successfully processed, the response will contain the processed data or a success message.

```json
{'reviews': [], 'status': 'failed', 'status_code': 500, 'error': 'Failed to scrape the reviews due to internal error'}
