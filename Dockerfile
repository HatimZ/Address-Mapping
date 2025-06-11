# Build stage for frontend
FROM node:22.16.0-alpine AS frontend-builder
WORKDIR /app/frontend
COPY front-end/package*.json ./
RUN npm install
COPY front-end/ ./
RUN npm run build

# Build stage for backend
FROM python:3.11-slim AS backend-builder
WORKDIR /app/backend
COPY back-end/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY back-end/ ./

# Production stage
FROM python:3.11-slim
WORKDIR /app

# Install nginx and node for running the SvelteKit server
RUN apt-get update && \
    apt-get install -y nginx curl && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Configure nginx
RUN rm -rf /etc/nginx/sites-enabled/default && \
    rm -rf /etc/nginx/sites-available/default

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create nginx log directory
RUN mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log && \
    touch /var/log/nginx/error.log

# Copy frontend build and node_modules
COPY --from=frontend-builder /app/frontend /app/frontend/


# Copy backend and install Python packages
COPY --from=backend-builder /app/backend /app/backend
COPY back-end/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt


# Set environment variables
ENV PYTHONPATH=/app/backend
ENV PORT=3000
ENV HOST=0.0.0.0

# Expose ports
EXPOSE 80

# Start all services
CMD service nginx start && \
    cd /app/backend && uvicorn src.main:app --host 0.0.0.0 --port 8000 & \
    cd /app/frontend && npm run preview -- --host 0.0.0.0 --port 3000 & \
    tail -f /var/log/nginx/error.log 