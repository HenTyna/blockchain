#!/bin/bash

echo "🚀 Starting Blockchain Research Project..."

# Check if Python and Node.js are installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

echo "✅ Python and Node.js found"

# Create virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

echo "✅ Dependencies installed successfully!"

# Start backend server
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
python api/main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🌐 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "🎉 Blockchain Research Project is running!"
echo ""
echo "📊 Backend API: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handler
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
