# BusFlow Project Report

## Abstract
BusFlow is a web-based bus ticket booking and seat allocation system. It brings bus search, schedule comparison, seat selection, passenger details and confirmation into one interface. The backend validates seat holds and prevents duplicate confirmed allocations.

## Problem statement
Fragmented booking workflows make route comparison and seat availability unclear. Manual allocation can cause duplicate assignments. BusFlow demonstrates a centralized workflow with database-backed validation.

## Objectives
1. Search sample bus services by route.
2. Display operator, timings, fare and seat availability.
3. Let passengers select seats interactively.
4. Prevent duplicate confirmed seat allocation.
5. Generate a booking reference and support lookup.
6. Demonstrate operator-side service and occupancy information.

## Modules
Passenger search; trip listing; seat allocation; temporary seat holds; passenger details; confirmation; ticket lookup; operator dashboard concept.

## Technology
Next.js, React and TypeScript; FastAPI; SQLAlchemy; SQLite; Pytest.

## Methodology
The browser displays seat status, but the backend is authoritative. The API creates short-lived holds, checks expiry on confirmation, and writes booking plus seat assignments in one transaction. A unique database constraint prevents a second confirmed booking for the same trip-seat pair.

## Limitations
The schedules and prices are synthetic. Payment is simulated. Authentication, real inventory, notifications, production deployment and refund workflows are outside the MVP.

## Future scope
Add user/operator login, PostgreSQL and migrations, PDF/QR tickets, payment sandbox, cancellation/refunds, notifications, live GPS and operator inventory integration.

## Conclusion
BusFlow demonstrates a booking workflow and practical concepts in UI design, REST APIs, relational modelling and transaction-safe seat allocation.
