#!/bin/bash

# Create necessary directories
mkdir -p logs

# Setup frontend
echo "Setting up frontend..."
cd front-end
npm install
npm run build
cd ..

# Setup backend
echo "Setting up backend..."
python -m venv venv
source venv/bin/activate
pip install -r back-end/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
NODE_ENV=development
PYTHONUNBUFFERED=1
EOL
fi

echo "Setup completed successfully!" 