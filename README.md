# Address Distance API

A FastAPI application for calculating distances between addresses and maintaining a history of queries.

## Features

- Calculate distances between two addresses
- Maintain history of distance calculations
- Input validation and sanitization
- Rate limiting
- Caching
- Pagination

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

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=address_distance
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org
NOMINATIM_USER_AGENT=AddressDistanceAPI/1.0
```

3. Run the application:

```bash
uvicorn src.main:app --reload
```

## Database

The application uses a database-agnostic interface that can work with any database. Currently implemented for MongoDB, but can be easily extended to support other databases like PostgreSQL.

## Testing

Run tests with pytest:

```bash
pytest
```

## License

MIT
