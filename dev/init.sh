#!/bin/bash

echo "Starting application initialization..."

# Change to the app directory
cd /app

# Install dependencies (let uv and bun handle caching)
echo "Installing dependencies..."
make install

# Add node_modules/.bin to PATH for vite command
export PATH="/app/frontend/node_modules/.bin:$PATH"

# Build frontend assets
echo "Building frontend assets..."
make vite-build

# Run database migrations
echo "Running database migrations..."
make migrate

# Create cache table if it doesn't exist
echo "Creating cache table..."
make createcachetable || echo "Cache table creation completed or skipped"

# Start supervisord
echo "Starting supervisord..."
exec uv run supervisord -c /etc/supervisor/supervisord.conf
