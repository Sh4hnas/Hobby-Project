#!/bin/bash

echo "🚀 Setting up AI Celebrity Generator..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

# Setup backend
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    echo "💡 Try installing system dependencies first:"
    echo "   Ubuntu/Debian: sudo apt-get install python3-dev libffi-dev libjpeg-dev zlib1g-dev"
    echo "   macOS: brew install jpeg"
    exit 1
fi

cd ..

echo "✅ Setup completed successfully!"
echo ""
echo "🎉 To start the application:"
echo "1. Backend: cd backend && source venv/bin/activate && python app.py"
echo "2. Frontend: npm start"
echo ""
echo "Or use the development script: npm run dev"