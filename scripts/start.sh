#!/bin/bash

# Grocery Price Checker - Start Script
# Quick start script for development

echo "🛒 Starting Grocery Price Checker..."
echo ""

# Check if setup has been run
if [ ! -f "grocery_app.db" ]; then
    echo "⚠️  Database not found. Running setup first..."
    ./scripts/setup.sh
    echo ""
fi

echo "🚀 Starting development server..."
echo ""
echo "Access points:"
echo "  • Web App: http://localhost:8000/app"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • API Alternative Docs: http://localhost:8000/redoc"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo ""

poetry run python run.py
