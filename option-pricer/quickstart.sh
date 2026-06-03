#!/bin/bash

# Option Pricer - Quick Start Script for macOS
# This script helps you quickly start both backend and frontend servers

echo "🚀 Option Pricer Quick Start"
echo "=============================="
echo ""

# Check if we're in the project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory (/Users/borjagarcia/option-pricer)"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."
if ! command_exists python3; then
    echo "❌ Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js not found. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Ask user what they want to do
echo "What would you like to do?"
echo "1) Setup backend (create venv and install dependencies)"
echo "2) Setup frontend (npm install)"
echo "3) Setup both"
echo "4) Start backend only"
echo "5) Start frontend only"
echo "6) Start both (in separate terminal windows)"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo "🔧 Setting up backend..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✅ Backend setup complete!"
        echo "To start the backend, run: cd backend && source venv/bin/activate && python3 main.py"
        ;;
    2)
        echo "🔧 Setting up frontend..."
        cd frontend
        npm install
        echo "✅ Frontend setup complete!"
        echo "To start the frontend, run: cd frontend && npm run dev"
        ;;
    3)
        echo "🔧 Setting up backend..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        cd ..
        echo "✅ Backend setup complete!"
        echo ""
        echo "🔧 Setting up frontend..."
        cd frontend
        npm install
        cd ..
        echo "✅ Frontend setup complete!"
        echo ""
        echo "To start the application:"
        echo "1. Backend: cd backend && source venv/bin/activate && python3 main.py"
        echo "2. Frontend: cd frontend && npm run dev"
        ;;
    4)
        echo "🚀 Starting backend..."
        cd backend
        if [ ! -d "venv" ]; then
            echo "❌ Virtual environment not found. Please run setup first (option 1 or 3)"
            exit 1
        fi
        source venv/bin/activate
        python3 main.py
        ;;
    5)
        echo "🚀 Starting frontend..."
        cd frontend
        if [ ! -d "node_modules" ]; then
            echo "❌ node_modules not found. Please run npm install first (option 2 or 3)"
            exit 1
        fi
        npm run dev
        ;;
    6)
        echo "🚀 Starting both servers..."
        echo ""
        echo "This will open two new terminal windows."
        echo "Make sure to grant Terminal permission if prompted."
        echo ""
        
        # Start backend in new terminal
        osascript -e "tell application \"Terminal\" to do script \"cd '$PWD/backend' && source venv/bin/activate && python3 main.py\""
        
        sleep 2
        
        # Start frontend in new terminal
        osascript -e "tell application \"Terminal\" to do script \"cd '$PWD/frontend' && npm run dev\""
        
        echo "✅ Both servers starting in new terminal windows!"
        echo "Backend: http://localhost:8000"
        echo "Frontend: http://localhost:5173"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1-6."
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"
