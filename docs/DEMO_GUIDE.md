# Demo Guide

1. Start the backend and run `python -m app.seed`.
2. Start the frontend with `npm run dev`.
3. Search a sample route, such as Hyderabad to Bengaluru.
4. Select a bus service and choose available seats.
5. Enter passenger details and continue.
6. Complete the clearly labelled simulated checkout.
7. Note the generated booking reference.
8. Open http://127.0.0.1:8000/docs to demonstrate the APIs.

All service data is synthetic. This demo does not process real payments or issue valid travel tickets.

## Find previous bookings

1. Scroll to the **Find your booking** section.
2. Enter the phone number and email address used at booking time.
3. Select **Show history** to display matching PNRs, trip routes, seats, status and fare.
4. Use the PNR search above to inspect one booking or the cancellation control to cancel it.

The history lookup matches both contact fields and returns up to 50 recent records. It is a demonstration feature, not a substitute for customer authentication.
