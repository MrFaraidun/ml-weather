#!/bin/bash

# --- STARTUP SCRIPT FOR WEATHER PREDICTION PROJECT ---

# Function to kill all background processes when you press Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Shutting down all services..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT

echo "🚀 Preparing project environment..."

# Automatically kill any old processes on our ports
echo "🧹 Clearing old processes on ports 3001, 5000, 5173..."
fuser -k 3001/tcp 2>/dev/null
fuser -k 5000/tcp 2>/dev/null
fuser -k 5173/tcp 2>/dev/null

echo "🚀 Starting Weather Prediction Project..."

# 1. Start ML Service (Flask)
echo "📂 Starting ML Service (Python on port 5000)..."
cd ml-service
source venv/bin/activate
python app.py &
cd ..

# 2. Start Middleware API (Node.js)
echo "📂 Starting Middleware Server (Express on port 3001)..."
cd server
npm run dev &
cd ..

# 3. Start Frontend (Vite/React)
echo "📂 Starting Frontend (Vite on port 5173)..."
cd client
npm run dev

# Wait for background processes
wait
