# BusFlow — C11 Console Bus Booking System

BusFlow is a simple college-project bus booking application written entirely in **standard C11**. It runs in a terminal and demonstrates basic menu-driven interaction, structures, arrays, functions, input validation, and file handling.

## Features

- Display sample bus routes, operators, timings, and fares
- Search buses by source and destination (case-insensitive)
- View a 2+2 seat layout and live seat availability
- Book one available seat with passenger name and mobile number
- Generate a demo PNR and display a booking confirmation
- Find an active booking using its PNR
- Cancel a booking after checking the booking mobile number
- View active booking history
- Save bookings between runs using a local binary data file

## Technology

- Language: ISO C11
- Standard library only: stdio.h, stdlib.h, string.h, ctype.h, errno.h, time.h
- Compiler: GCC or another C11-compatible compiler
- Storage: local file, busflow_bookings.dat

There is no Python, JavaScript, TypeScript, database server, web framework, or third-party library.

## Compile and run

### Linux

~~~bash
gcc -std=c11 -Wall -Wextra -pedantic -O2 busflow.c -o busflow
./busflow
~~~

### Windows (MinGW GCC)

~~~bash
gcc -std=c11 -Wall -Wextra -pedantic -O2 busflow.c -o busflow.exe
busflow.exe
~~~

### macOS

~~~bash
clang -std=c11 -Wall -Wextra -pedantic -O2 busflow.c -o busflow
./busflow
~~~

The program creates busflow_bookings.dat in its current working directory when the first booking is saved. Keep that file if you want booking records to remain available the next time you run the program.

## Menu

1. Display all buses
2. Search buses by route
3. View seat availability
4. Book a seat
5. Find booking using PNR
6. Cancel a booking
7. View booking history
0. Exit

## Sample routes

| Operator | Route | Departure | Arrival | Fare |
|---|---|---:|---:|---:|
| Metro Travels | Hyderabad – Bengaluru | 21:00 | 06:00 | ₹1,499 |
| Orange Express | Hyderabad – Vijayawada | 07:00 | 13:00 | ₹799 |
| Kaveri Lines | Hyderabad – Chennai | 22:00 | 08:00 | ₹1,299 |
| Deccan Roadways | Hyderabad – Warangal | 08:30 | 11:30 | ₹399 |

## Project report\n\nA CPDS laboratory report template following the supplied reference structure is available at [docs/CPDS_PROJECT_REPORT.md](docs/CPDS_PROJECT_REPORT.md). Replace all bracketed identity and faculty fields, and insert screenshots and the complete current source listing before submission.\n\n## Project notes

- Routes and fares are synthetic sample data.
- A booking is a classroom demonstration only. No payment is collected and no real travel ticket is issued.
- The booking file stores C structures in binary form. Use the same program/compiler environment when continuing with an existing data file.
- To reset the demonstration, close the program and delete busflow_bookings.dat.

## Repository structure

~~~text
Bus-flow/
├── busflow.c
├── README.md
├── LICENSE
└── docs/
    ├── CPDS_PROJECT_REPORT.md
    ├── DEMO_GUIDE.md
    ├── PROJECT_REPORT.md
    └── SYSTEM_DESIGN.md
~~~
