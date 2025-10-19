#!/bin/bash

echo "🚀 Starting Multi-Agent Orchestrator..."

# With Docker Compose
echo "Starting with Docker Compose..."
docker-compose up -d

# Check services
echo "Checking services..."
docker-compose ps

echo "✅ Services started!"
echo "📍 Web Interface: http://localhost:5000"
echo "🗄️  Database: PostgreSQL on port 5432"
echo "💾 Cache: Redis on port 6379"
