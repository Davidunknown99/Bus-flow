# BusFlow Project Report

## Abstract

BusFlow is a menu-driven bus booking application implemented entirely in standard C11. It demonstrates route search, seat availability, passenger booking, PNR lookup, cancellation, and persistent booking history through a simple terminal interface.

## Problem statement

A basic booking demonstration should let a user inspect sample bus routes, choose a seat, record passenger details, and retrieve or cancel a booking without requiring a web server or database setup.

## Objectives

1. Display sample buses, routes, timings, and fares.
2. Search routes by source and destination.
3. Display a 2+2 seat layout and mark booked seats.
4. Book an available seat and collect passenger details.
5. Generate a booking reference (PNR).
6. Find and cancel bookings.
7. Preserve booking records between program runs.

## Technology

- ISO C11
- GCC or another C11-compatible compiler
- C standard library only
- Structures, arrays, functions, string handling, and file I/O
- Local binary file for booking persistence

## Modules

- Bus listing and route search
- Seat availability display
- Seat booking and confirmation
- PNR lookup
- Booking cancellation with phone-number check
- Active booking history
- File-based save and load

## Methodology

The program stores sample bus information in a constant array of structures. Booking records are held in an array of structures. A seat is unavailable when an active booking exists for the same bus and seat number. Each successful booking is written to busflow_bookings.dat. Cancellation changes the booking status and saves the updated records, making the seat available again.

## Limitations

The bus routes and fares are synthetic. The program is intended for a local classroom demonstration. It does not process payments, issue valid travel tickets, or provide multi-user network access. Binary data files are intended to be reused with a compatible build of this program.

## Conclusion

BusFlow demonstrates core C programming concepts in a practical booking scenario while keeping compilation and execution straightforward.
