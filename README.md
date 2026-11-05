# BusFlow — College Project

A bus ticket booking and seat allocation demo. Frontend: Next.js + TypeScript. Backend: FastAPI + SQLAlchemy + SQLite. Includes sample trips, interactive seats, expiring holds and PNR confirmation. Payment is simulated only.

## Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

## Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:3000. See docs/PROJECT_REPORT.md and docs/DEMO_GUIDE.md.
