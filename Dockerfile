# Build stage for frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY front-end/package*.json ./
RUN npm ci
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

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy frontend build
COPY --from=frontend-builder /app/frontend/.svelte-kit/output /app/frontend/.svelte-kit/output

# Copy backend
COPY --from=backend-builder /app/backend /app/backend
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Set environment variables
ENV PYTHONPATH=/app/backend
ENV PORT=3000

# Expose ports
EXPOSE 80

# Start both nginx and backend
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"] 