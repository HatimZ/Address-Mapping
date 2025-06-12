# Address Distance API

A FastAPI application for calculating distances between addresses and maintaining a history of queries.

## Features

- Calculate distances between two addresses
- Maintain history of distance calculations
- Input validation and sanitization
- Rate limiting
- Caching
- Pagination

## How to Run

### Overview

This project uses a single Docker container to build and run both the frontend (SvelteKit) and backend (FastAPI) for simplicity.

- **nginx** is used as a reverse proxy:

  - Requests to `/` are routed to the SvelteKit frontend server (running on port 3000).
  - Requests starting with `/api` are routed to the FastAPI backend server (running on port 8000).

- **Frontend**: SvelteKit runs in preview mode for simplicity.
- **Backend**: FastAPI runs on a Uvicorn server.

### API Domain Configuration

- The frontend has a `config.ts` file in `src/lib/api/` which specifies the backend API domain URL.
- If running locally, set this variable to `http://localhost`.
- In production, it points to the load balancer URL (see below).

### Running Locally

1. **Prepare your environment variables**  
   Create an `.env` file at the project root with the following variables

   ```env
   MONGODB_USERNAME=
   MONGODB_PASSWORD=
   MONGODB_URL=
   PUBLIC_API_URL=
   APP_NAME=
   VERSION=
   API_PREFIX=
   NOMINATIM_BASE_URL=
   NOMINATIM_USER_AGENT=
   ```

2. **Build and run the Docker image**

   ```bash
   docker build . -t address-distance-app
   docker run -p 80:80 address-distance-app
   ```

   This will start both the frontend and backend, accessible at [http://localhost](http://localhost).

3. **Frontend routes**

   - `/` — Calculation page
   - `/history` — Historical queries page

4. **Backend routes**

   - `/api/v1/distance/calculate` — Calculate distance (POST)
   - `/api/v1/history` — Fetch historical results (GET)

5. **API Documentation**
   - OpenAPI docs are available at `/api/v1/docs` for interactive API testing.

### Production Deployment

- Production deployment is done on AWS ECS with Fargate.
- The app is served behind a load balancer.
- The frontend's `config.ts` uses the load balancer URL for backend API requests.

**Summary:**

- All services run in a single Docker container for simplicity.
- nginx routes requests to the correct service.
- SvelteKit runs in preview mode, FastAPI runs on Uvicorn.
- Configure your backend API URL in the frontend's `config.ts`.
- Use an `.env` file for all required environment variables.
- OpenAPI docs are available at `/api/v1/docs`.

## Implementation Details

### Security

- Input sanitization for addresses before sending to third-party geocoding API
- SQL injection prevention
- XSS protection
- Command injection prevention
- HTML/script injection prevention

### Rate Limiting

- Distance calculation: 5 requests per minute
- History retrieval: 100 requests per minute
- IP-based rate limiting
- Configurable limits

### Caching Strategy

- Distance calculations cached by address pairs (1-hour TTL)
- History list cached by page and page size (1-hour TTL)
- Automatic cache invalidation:
  - New distance calculation invalidates history cache
  - Each address pair has its own cache entry
  - Cache keys based on input parameters

### Pagination

- History endpoint supports pagination
- Configurable page size (1-100 records)
- Page number starts at 1
- Returns total count and total pages
- Sorted by timestamp (newest first)

## API Endpoints

### Calculate Distance

```http
POST /api/v1/distance/calculate
```

Calculate distance between two addresses.

### Get History

```http
GET /api/v1/history?page=1&page_size=10
```

Get paginated history of distance calculations.

## Database

The application uses a database-agnostic interface that can work with any database. Currently implemented for MongoDB, but can be easily extended to support other databases like PostgreSQL.

## Testing

Run tests with pytest:

```bash
pytest
```

## License

MIT
