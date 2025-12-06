# Online Coding Interview Platform

## Project Structure
- `frontend/`: React + Vite + TypeScript application
- `backend/`: FastAPI + Python application

## Getting Started

You need to run the backend and frontend in separate terminals.

### 1. Start the Backend
```bash
cd backend
# Install dependencies (if not already done)
pip install -r requirements.txt
# Run the server
python -m uvicorn main:app --reload --port 8000
```
The backend will run at http://localhost:8000.

### 2. Start the Frontend
Open a new terminal:
```bash
cd frontend
# Install dependencies (if not already done)
npm install
# Run the dev server
npm run dev
```
The frontend will run at http://localhost:5173.

## Features
- **Real-time Collaboration**: Share the URL to invite others.
- **Code Execution**: Run JavaScript/Python code safely in the browser.
- **Dark Mode**: Premium coding experience.
