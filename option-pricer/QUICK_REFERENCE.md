# Quick Reference - Option Pricer

## Essential Commands

### First Time Setup

```bash
# 1. Backend Setup
cd /Users/borjagarcia/option-pricer/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Frontend Setup
cd /Users/borjagarcia/option-pricer/frontend
npm install
```

### Daily Development

**Option 1: Use the Quick Start Script**
```bash
cd /Users/borjagarcia/option-pricer
./quickstart.sh
```

**Option 2: Manual Start**

*Terminal 1 - Backend:*
```bash
cd /Users/borjagarcia/option-pricer/backend
source venv/bin/activate
python3 main.py
```

*Terminal 2 - Frontend:*
```bash
cd /Users/borjagarcia/option-pricer/frontend
npm run dev
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### Stopping the Servers

Press `Ctrl + C` in each terminal window

To deactivate Python environment:
```bash
deactivate
```

## Troubleshooting Quick Fixes

### Backend Issues

**Port 8000 in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Missing Python packages:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

**Dependencies out of sync:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Clear Vite cache:**
```bash
rm -rf node_modules/.vite
npm run dev
```

**Port 5173 in use:**
```bash
npm run dev -- --port 3000
```

### Full Reset

```bash
# Backend
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
rm -rf node_modules package-lock.json
npm install
```

## Project Structure Quick View

```
option-pricer/
├── backend/
│   ├── main.py           # FastAPI app
│   ├── requirements.txt  # Python dependencies
│   └── venv/            # Virtual environment
├── frontend/
│   ├── src/             # React source
│   ├── package.json     # npm dependencies
│   └── node_modules/    # Installed packages
├── README.md            # Full documentation
├── quickstart.sh        # Quick start script
└── QUICK_REFERENCE.md   # This file
```

## Common Tasks

### Update Dependencies

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install --upgrade fastapi uvicorn numpy scipy
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm update
```

### Build for Production

```bash
cd frontend
npm run build
npm run preview
```

### View Logs

Backend logs appear in the terminal where `python3 main.py` is running.
Frontend logs appear in the browser console (F12 → Console tab).

## Keyboard Shortcuts

- **Stop server**: `Ctrl + C`
- **Clear terminal**: `Cmd + K`
- **New terminal tab**: `Cmd + T`
- **Browser DevTools**: `F12` or `Cmd + Option + I`

## Environment Variables

If using environment variables, create these files:

**Backend** (`backend/.env`):
```bash
PORT=8000
HOST=0.0.0.0
```

**Frontend** (`frontend/.env`):
```bash
VITE_API_URL=http://localhost:8000
```

## Need Help?

See the [full README](README.md) for:
- Detailed installation instructions
- Feature documentation
- Comprehensive troubleshooting
- API documentation links
