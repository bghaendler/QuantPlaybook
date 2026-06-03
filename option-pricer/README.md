# Option Pricer Application

A comprehensive options pricing application with a FastAPI backend and React frontend. This application implements various option pricing models including Black-Scholes-Merton, barrier options, and exotic options with real-time calculations and visualization.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
  - [Starting the Backend](#starting-the-backend)
  - [Starting the Frontend](#starting-the-frontend)
- [Project Structure](#project-structure)
- [Features](#features)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed on your macOS:

### 1. Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Python 3.8 or higher
```bash
# Install Python using Homebrew
brew install python3

# Verify installation
python3 --version
```

### 3. Node.js and npm (version 16 or higher)
```bash
# Install Node.js using Homebrew
brew install node

# Verify installation
node --version
npm --version
```

## Installation

### Backend Setup

1. **Navigate to the backend directory:**
```bash
cd /Users/borjagarcia/option-pricer/backend
```

2. **Create a Python virtual environment:**
```bash
python3 -m venv venv
```

3. **Activate the virtual environment:**
```bash
source venv/bin/activate
```

4. **Install required Python packages:**
```bash
pip install fastapi uvicorn numpy scipy python-multipart
```

Alternatively, if a `requirements.txt` file exists:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. **Navigate to the frontend directory:**
```bash
cd /Users/borjagarcia/option-pricer/frontend
```

2. **Install npm dependencies:**
```bash
npm install
```

This will install all the required packages including:
- React 19.2.0
- Vite (via rolldown-vite)
- Plotly.js for data visualization
- Axios for API calls
- And other dependencies specified in `package.json`

## Running the Application

You'll need **two terminal windows** to run both the backend and frontend simultaneously.

### Starting the Backend

**Terminal 1 - Backend:**

1. Navigate to the backend directory:
```bash
cd /Users/borjagarcia/option-pricer/backend
```

2. Activate the virtual environment (if not already activated):
```bash
source venv/bin/activate
```

3. Start the FastAPI server:
```bash
python3 main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start on: **http://localhost:8000**

You should see output similar to:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Starting the Frontend

**Terminal 2 - Frontend:**

1. Navigate to the frontend directory:
```bash
cd /Users/borjagarcia/option-pricer/frontend
```

2. Start the development server:
```bash
npm run dev
```

The frontend will start on: **http://localhost:5173** (or another port if 5173 is busy)

You should see output similar to:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

3. Open your browser and navigate to the URL shown (typically **http://localhost:5173**)

## Project Structure

```
option-pricer/
├── backend/
│   ├── main.py              # FastAPI application with pricing engine
│   └── venv/                # Python virtual environment (created during setup)
│
├── frontend/
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration
│   └── node_modules/        # npm packages (created during npm install)
│
└── README.md                # This file
```

## Features

The application includes:

- **Multiple Option Pricing Models:**
  - Black-Scholes-Merton (BSM)
  - Merton (Continuous Dividend)
  - Black-76 (Futures Options)
  - Garman-Kohlhagen (FX Options)
  - Asay (Margined Futures)
  - Brenner-Subrahmanyam Approximation
  - **Bachelier (1900) Arithmetic** - [See detailed docs](BACHELIER_MODEL.md)
  - Standard Barrier Options (Up/Down, In/Out)
  - Black-76F (Deferred Settlement)

- **Real-time Calculations:**
  - Option pricing
  - Greeks (Delta, Gamma, Vega, Theta, Rho)
  - Interactive charts and visualizations

- **Visualizations:**
  - Price vs Spot graphs
  - Greeks sensitivity analysis
  - Volatility surface heatmaps
  - Probability distribution curves

## Troubleshooting

### Backend Issues

**Problem: `ModuleNotFoundError` for FastAPI, numpy, or scipy**
```bash
# Make sure you've activated the virtual environment
source venv/bin/activate

# Reinstall the package
pip install fastapi uvicorn numpy scipy
```

**Problem: Port 8000 already in use**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or start on a different port
uvicorn main:app --reload --port 8001
```

**Problem: CORS errors in browser console**
- The backend is already configured with CORS middleware to allow all origins
- Ensure the backend is running before starting the frontend

### Frontend Issues

**Problem: `npm install` fails**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**Problem: Port 5173 already in use**
- Vite will automatically try the next available port (5174, 5175, etc.)
- Or you can specify a port: `npm run dev -- --port 3000`

**Problem: Cannot connect to backend API**
- Verify the backend is running on http://localhost:8000
- Check the frontend API configuration (likely in a config file or environment variable)
- Look for `VITE_API_URL` or similar in the frontend code

**Problem: Build errors with Vite**
```bash
# Try clearing Vite cache
rm -rf node_modules/.vite

# Restart the dev server
npm run dev
```

### General Issues

**Problem: Permission denied when installing packages**
```bash
# For Python packages, make sure virtual environment is activated
source venv/bin/activate

# For npm, you might need to fix permissions
sudo chown -R $(whoami) ~/.npm
```

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Build

To create a production build of the frontend:

```bash
cd /Users/borjagarcia/option-pricer/frontend
npm run build
```

The optimized files will be in the `dist` directory.

To preview the production build:
```bash
npm run preview
```

## Stopping the Application

To stop the application:

1. **Backend**: Press `Ctrl+C` in the terminal running the backend
2. **Frontend**: Press `Ctrl+C` in the terminal running the frontend
3. **Deactivate Python virtual environment**: Type `deactivate` in the backend terminal

## Additional Notes

- The backend runs on **port 8000** by default
- The frontend runs on **port 5173** by default (Vite's default)
- Both servers support hot-reload during development:
  - Backend: Changes to Python files automatically restart the server
  - Frontend: Changes to React files automatically refresh the browser

## Support

For issues or questions, please review the troubleshooting section or check the respective documentation for:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
