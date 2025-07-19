#!/bin/bash

# AI Image Generator Frontend Startup Script

echo "🎨 Starting AI Image Generator Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Please run this script from the project root directory."
    exit 1
fi

# Change to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the development server
echo "🌐 Starting React development server..."
echo "📖 Frontend will be available at: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo ""
echo "Make sure the backend is running first!"
echo "Press Ctrl+C to stop the server"
echo ""

npm start