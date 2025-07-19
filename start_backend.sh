#!/bin/bash

# AI Image Generator Backend Startup Script

echo "🚀 Starting AI Image Generator Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Please run this script from the project root directory."
    exit 1
fi

# Change to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "🌐 Starting FastAPI server..."
echo "📖 API documentation will be available at: http://localhost:8000/docs"
echo "🔗 Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py