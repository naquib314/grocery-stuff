#!/bin/bash

# Grocery Price Checker - Setup Script
# This script sets up the development environment

set -e

echo "🛒 Setting up Grocery Price Checker..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "✅ Poetry found"

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Set up environment file
if [ ! -f .env ]; then
    echo "🔧 Creating environment file..."
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
else
    echo "✅ .env file already exists"
fi

# Run database migrations
echo "🗄️  Setting up database..."
poetry run alembic upgrade head

# Load dummy data
echo "📊 Loading sample data..."
poetry run python -m app.load_data

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "  poetry run python run.py"
echo ""
echo "Or use the quick start script:"
echo "  ./scripts/start.sh"
echo ""
echo "Access points:"
echo "  • Web App: http://localhost:8000/app"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Health Check: http://localhost:8000/health"
echo ""
