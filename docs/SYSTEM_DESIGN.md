# System Design

```text
Passenger UI (Next.js) -> FastAPI REST API -> SQLAlchemy -> SQLite
```

## Entities
Trip: operator, bus, route, times, fare and layout. Seat: per-trip seat identity. Hold: owner, seat IDs, idempotency key, expiry and state. Booking: PNR and passenger details. BookingSeat: confirmed trip-seat association.

## Seat state machine
AVAILABLE -> HELD -> BOOKED; HELD -> AVAILABLE after expiry or release.

## Invariants
- Frontend status is advisory; backend writes determine allocation.
- Holds are all-or-nothing for the submitted seat set.
- Server time controls expiry.
- Reusing an idempotency key with a different payload is a conflict.
- Confirmation validates hold ownership and expiry before writing booking plus seat rows in one transaction.
- Unique (trip_id, seat_id) constraint prevents duplicate confirmed assignment.

## API
GET /health; GET /api/v1/trips; GET /api/v1/trips/{id}/seats; POST /api/v1/holds; POST /api/v1/holds/{id}/confirm; GET /api/v1/bookings/{pnr}.

## Production extension
Use PostgreSQL, migrations, authentication/authorization, rate limits, hosted payment checkout with signed webhook verification, monitoring, audit logs, privacy controls, backups and load tests. SQLite and simulated checkout are for a local college demo.
