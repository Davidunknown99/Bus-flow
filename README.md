# BusFlow — Bus Ticket Booking & Seat Allocation

A full-stack college project demonstrating bus search, interactive seat selection, temporary seat holds, passenger details and PNR confirmation.

## Stack
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Tests:** Pytest + FastAPI TestClient

## Features
- Search buses by origin and destination
- View schedules, operators, fares and bus layouts
- Interactive seat map with available / held / booked states
- Hold up to six seats for five minutes
- Passenger details and PNR confirmation
- Retrieve an existing booking by PNR
- Protected admin operations summary (trip, seat, booking, active-hold and demo revenue metrics)
- API documentation through Swagger UI

> **Academic demo:** routes and fares are synthetic. Confirmation is simulated; no real payment or valid travel ticket is issued.

## Run locally

### 1. Backend
Use Python 3.10+.

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
# Optional: enable the protected admin summary endpoint
# Set a strong secret in your environment before starting the API.
# macOS/Linux: export BUSFLOW_ADMIN_API_KEY='replace-with-a-long-random-secret'
# PowerShell: $env:BUSFLOW_ADMIN_API_KEY='replace-with-a-long-random-secret'
uvicorn app.main:app --reload
```

Backend: http://localhost:8000  
API docs: http://localhost:8000/docs

### 2. Frontend
In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. The frontend expects the API at http://localhost:8000. To change it, set `NEXT_PUBLIC_API_URL`.

### 3. Run backend tests
From the `backend` directory:

```bash
pytest
```

## Project documentation
- [Project report](docs/PROJECT_REPORT.md)
- [System design](docs/SYSTEM_DESIGN.md)
- [Demo guide](docs/DEMO_GUIDE.md)

## Admin summary API

`GET /api/v1/admin/summary` returns aggregate operational metrics. It is disabled unless `BUSFLOW_ADMIN_API_KEY` is configured, and requires that value in the `X-Admin-Key` request header. Do not expose this shared-key demo mechanism as production authentication; use individual accounts, role-based authorization and secret management before deployment.

## Important design note
The backend is authoritative for seat availability. It creates expiring holds and confirms a booking in a database transaction. A unique constraint on `(trip_id, seat_id)` in confirmed bookings is a final safeguard against duplicate allocation. SQLite is suitable for the local classroom demonstration; production deployment should use PostgreSQL and stronger concurrency controls.

## Future scope
Individual authentication and roles, full operator/admin dashboard, cancellation and refunds, PDF/QR tickets, payment sandbox, email/SMS notifications, PostgreSQL migrations and deployment.
