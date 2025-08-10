#!/usr/bin/env python3
"""
Grocery Price Checker - Main Entry Point

This script starts the FastAPI server and ensures the database is properly set up.
"""

import os
import sys
import uvicorn
from app.load_data import load_dummy_data

def main():
    """Main entry point for the application"""
    
    print("🛒 Starting Grocery Price Checker...")
    
    # Load dummy data if database is empty
    print("📊 Loading data...")
    load_dummy_data()
    
    # Get configuration from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    print(f"🚀 Starting server at http://{host}:{port}")
    print(f"📱 Web app available at: http://localhost:{port}/app")
    print(f"📖 API documentation: http://localhost:{port}/docs")
    print(f"🔧 Alternative docs: http://localhost:{port}/redoc")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        access_log=True
    )

if __name__ == "__main__":
    main()
