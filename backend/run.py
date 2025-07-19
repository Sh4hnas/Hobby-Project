#!/usr/bin/env python3
"""
Run script for the AI Image Generator backend
"""

import uvicorn
from config import API_HOST, API_PORT, DEBUG

if __name__ == "__main__":
    print(f"Starting AI Image Generator backend on {API_HOST}:{API_PORT}")
    print(f"Debug mode: {DEBUG}")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG,
        log_level="info"
    )