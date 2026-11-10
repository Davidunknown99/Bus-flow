# BusFlow — C11 Bus Booking Application

A terminal-based bus booking application written in standard C11.

## Features
- Display sample bus routes, timings and fares
- Search routes by origin and destination
- View 24-seat availability in a 2+2 layout
- Book a seat with passenger name and mobile number
- Generate and look up a PNR
- Cancel a booking after mobile-number verification
- View active booking history
- Save and reload bookings using `busflow_bookings.dat`

## Build and run

```bash
gcc -std=c11 -Wall -Wextra -Werror -pedantic -O2 busflow.c -o busflow
./busflow
```

Windows (MinGW):

```bash
gcc -std=c11 -Wall -Wextra -Werror -pedantic -O2 busflow.c -o busflow.exe
busflow.exe
```

Routes and fares are sample data. This is an academic console application; it does not process payments or issue real tickets.
