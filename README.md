# Address Distance API

A FastAPI-based service that calculates distances between addresses using geocoding and provides search history functionality.

## Features

- Address geocoding using Nominatim
- Distance calculation between addresses
- Search history tracking
- MongoDB integration
- Rate limiting and security features
- Comprehensive error handling
- Production-grade logging

## Requirements

- Python 3.12
- MongoDB
- Docker (optional)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/address-distance-api.git
cd address-distance-api
```

2. Create and activate virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements/base.txt
```

4. Create `.env` file:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_DATABASE=address_distance
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org
NOMINATIM_USER_AGENT=AddressDistanceAPI/1.0
```

5. Run the application:

```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

## Docker Setup

1. Build the image:

```bash
docker build -t address-distance-api .
```

2. Run the container:

```bash
docker run -p 8000:8000 address-distance-api
```

## API Documentation

Once the application is running, you can access:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## API Endpoints

### Calculate Distance

```http
POST /api/v1/distance/calculate
Content-Type: application/json

{
    "address1": "New York, NY",
    "address2": "Los Angeles, CA"
}
```

### Get History

```http
GET /api/v1/history?limit=10
```

## Testing

Run the test suite:

```bash
pytest
```

Run specific test categories:

```bash
pytest -m unit  # Unit tests
pytest -m integration  # Integration tests
```

## Project Structure

```
address-mapping/
├── src/
│   ├── distance/          # Distance calculation module
│   ├── history/           # Query history module
│   ├── geocoding/         # Geocoding service
│   ├── database/          # Database client
│   └── main.py           # Application entry point
├── tests/
│   ├── distance/         # Distance tests
│   ├── history/          # History tests
│   └── integration/      # Integration tests
├── requirements/
│   └── base.txt         # Dependencies
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
