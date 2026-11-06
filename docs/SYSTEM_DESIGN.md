# BusFlow C11 System Design

## Architecture

~~~text
Terminal menu
    |
    v
Input and menu functions
    |
    +--> Bus listing and route search (static Bus array)
    |
    +--> Seat availability (active Booking records)
    |
    +--> Booking / PNR / cancellation
    |
    v
Booking array in memory
    |
    v
busflow_bookings.dat (C standard file I/O)
~~~

## Data structures

### Bus

Stores bus ID, operator, bus name, origin, destination, departure time, arrival time, and fare.

### Booking

Stores active/cancelled status, PNR, bus ID, seat number, passenger name, phone number, and fare.

## Booking flow

1. User chooses a bus.
2. The application displays its 24-seat layout.
3. User selects an available seat.
4. Passenger name and mobile number are collected.
5. A PNR is generated and the booking is saved to the local data file.

## Cancellation flow

1. User enters a PNR.
2. The program finds the matching active booking.
3. The booking mobile number is checked.
4. The booking is marked inactive and the data file is rewritten.
5. The seat becomes available because only active bookings occupy seats.

## Constraints and limitations

- One local process is intended to use the data file at a time.
- Sample routes and fares are compiled into the program.
- The binary file stores C structures and should be used with a compatible build.
- This is a classroom prototype, not a production ticketing service.
