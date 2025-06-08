#!/bin/bash

# Check Python version
python_version=$(python3 --version)
if [[ ! $python_version == *"Python 3.12"* ]]; then
    echo "Error: Python 3.12 is required"
    echo "Current version: $python_version"
    exit 1
fi

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements/base.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "MONGODB_URL=mongodb://localhost:27017" > .env
    echo "MONGODB_USERNAME=hatimzahid1995" >> .env
    echo "MONGODB_PASSWORD=zD3KvZ7quY2xf77t" >> .env
    echo "MONGODB_DATABASE=address_distance" >> .env
    echo "NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org" >> .env
    echo "NOMINATIM_USER_AGENT=AddressDistanceAPI/1.0" >> .env
fi

# Run the application
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000 