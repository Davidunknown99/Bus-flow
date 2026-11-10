# BUSFLOW — BUS BOOKING SYSTEM
## CPDS Laboratory Project Report

> **Submission template:** Replace every square-bracketed field with verified college, student, and faculty details before printing. Do not submit this template with placeholders.

---

# TITLE PAGE

**A LABORATORY PROJECT REPORT**

**ON**

# BUSFLOW — BUS BOOKING SYSTEM

Submitted in partial fulfilment of the requirements for the  
**COMPUTER PROGRAMMING AND DATA STRUCTURES (CPDS) LABORATORY**

for the award of the degree of

**BACHELOR OF TECHNOLOGY**

in

**CHEMICAL ENGINEERING**

Submitted by:

- [Student name] — [Roll number]
- [Additional team member, if applicable] — [Roll number]

Under the guidance of

**[Faculty guide name]**  
[Designation], [Department]

**B. V. RAJU INSTITUTE OF TECHNOLOGY**  
Narsapur, Medak District, Telangana — 502313

Academic Year: **2026–2027**

---

# CERTIFICATE

This is to certify that the laboratory project entitled **“BUSFLOW — BUS BOOKING SYSTEM”** is a bonafide work carried out by **[student name(s) and roll number(s)]** of the Department of **Chemical Engineering**, B. V. Raju Institute of Technology, in partial fulfilment of the requirements of the **Computer Programming and Data Structures Laboratory** during the academic year **2026–2027**, under my guidance.

The work presented in this report is, to the best of my knowledge, an account of the student's work completed for the stated laboratory project.

**[Faculty guide name]**  
Project Guide

**[Head of Department name]**  
Head of the Department

Date: [DD/MM/YYYY]  
Place: BVRIT, Narsapur

---

# CANDIDATE'S DECLARATION

We hereby declare that the project entitled **“BUSFLOW — BUS BOOKING SYSTEM”** submitted as part of the Computer Programming and Data Structures Laboratory is our work, carried out under the guidance of **[faculty guide name]**.

We further declare that this report has been prepared for academic evaluation and that any external material used has been acknowledged in the references.

Student signature(s):

1. [Student name] — [Roll number]
2. [Additional team member, if applicable] — [Roll number]

Date: [DD/MM/YYYY]

---

# ACKNOWLEDGEMENT

We express our sincere gratitude to **[faculty guide name]**, [designation], for the guidance and feedback provided during the development of this laboratory project.

We thank the Head of the Department, faculty members, and the management of B. V. Raju Institute of Technology for providing the academic environment and resources required to complete this work.

We also acknowledge the official C language and compiler documentation consulted while implementing and testing the program.

**[Student name(s)]**

---

# ABSTRACT

**BusFlow** is a menu-driven bus booking application developed in the C programming language using the ISO C11 standard. The project demonstrates how fundamental programming concepts can be applied to a practical reservation workflow. Users can view sample bus routes, search for buses by origin and destination, inspect seat availability, book a seat, retrieve a booking using its Passenger Name Record (PNR), cancel a booking after a mobile-number check, and view active booking history.

The program uses structures and arrays to represent bus and booking information, functions to separate application operations, input validation to handle user entries, and standard file handling to preserve booking records between program executions. A local binary file is used for persistence, so a database server or external library is not required.

The project is intended as an academic demonstration of menu-driven programming, modular design, data management, conditional logic, loops, string handling, and file I/O in C. The included routes and fares are sample data; the application does not process payments or issue real travel tickets.

---

# 1. INTRODUCTION

## 1.1 Overview

Bus reservation involves selecting a route, checking seat availability, recording passenger information, and maintaining a booking reference. BusFlow models this workflow in a simple terminal-based application.

The application is written in standard C11 and uses a menu so that a user can perform one operation at a time. The program is designed to be compiled with a C11-compatible compiler and run locally.

## 1.2 Features of BusFlow

- **Bus listing:** Displays the available sample buses, routes, timings, and fares.
- **Route search:** Searches for buses using source and destination; matching is case-insensitive.
- **Seat availability:** Displays a 24-seat layout in a 2+2 arrangement. The symbol X indicates a booked seat.
- **Seat booking:** Allows a passenger to select an available seat and enter a name and mobile number.
- **PNR generation:** Generates a booking reference for a successful demonstration booking.
- **PNR lookup:** Retrieves an active booking using its PNR.
- **Cancellation:** Checks the booking's mobile number before marking the booking cancelled.
- **Booking history:** Displays active booking records.
- **File storage:** Saves booking records locally so they can be loaded during a later execution.

---

# 2. PROJECT DEFINITION

## 2.1 Project title

**BusFlow — Bus Booking System**

## 2.2 Problem statement

A basic bus-booking demonstration requires a clear way to browse routes, check seat availability, record a passenger's seat selection, and retrieve or cancel a reservation. BusFlow implements these operations in a standalone C console program without requiring a web server or database installation.

## 2.3 Objectives

1. Develop a menu-driven application using standard C11.
2. Represent buses and bookings using structures.
3. Display sample bus information and search by route.
4. Track seat availability and prevent an active seat from being booked again.
5. collect passenger details and generate a PNR for a booking.
6. Support booking retrieval and cancellation.
7. Store and reload booking records using file handling.
8. Demonstrate modular programming through separate functions.

---

# 3. SCOPE OF THE WORK

The project covers local, single-program bus-booking operations using predefined sample routes. It includes bus display, route search, seat selection, booking creation, PNR lookup, cancellation, active booking history, and local persistence.

The project is limited to an academic console demonstration. It does not include live bus-operator inventory, online user accounts, payment-gateway integration, SMS notifications, a networked database, or legally valid travel tickets. The routes and fares are illustrative sample data.

---

# 4. SYSTEM DESIGN AND IMPLEMENTATION

## 4.1 Development environment

| Component | Description |
|---|---|
| Programming language | ISO C11 |
| Compiler | GCC or another C11-compatible compiler |
| Interface | Command-line / terminal menu |
| Data representation | C structures and arrays |
| Persistence | Local binary file: `busflow_bookings.dat` |
| External libraries | None |

## 4.2 Main modules

1. **Bus display and search:** Reads the predefined bus array and filters routes.
2. **Seat map:** Checks active bookings to show seat status.
3. **Booking:** Collects bus, seat, and passenger details, then creates a PNR.
4. **PNR search:** Locates an active booking by its reference.
5. **Cancellation:** Verifies the mobile number and changes the booking status.
6. **Booking history:** Lists active bookings.
7. **Persistence:** Loads records at startup and saves changes to the local data file.

## 4.3 Data structures

The application uses a bus structure to hold the bus identifier, operator, bus name, origin, destination, departure and arrival times, and fare.

A booking structure stores the booking status, PNR, bus identifier, seat number, passenger name, mobile number, and fare. Arrays of these structures are used for in-memory data management.

## 4.4 Booking workflow

1. The user selects the bus listing or route-search option.
2. The user selects a bus and opens its seat map.
3. The user chooses a seat that is not already booked.
4. The program collects passenger details.
5. The program generates a PNR and saves the booking.
6. The confirmation details are displayed.

## 4.5 Cancellation workflow

1. The user enters the PNR.
2. The program searches for the corresponding active booking.
3. The user supplies the mobile number recorded for that booking.
4. If the check succeeds, the booking is marked cancelled and the updated records are saved.
5. The seat is then shown as available.

## 4.6 Compilation and execution

Linux / macOS:

```bash
gcc -std=c11 -Wall -Wextra -Werror -pedantic -O2 busflow.c -o busflow
./busflow
```

Windows with MinGW GCC:

```bash
gcc -std=c11 -Wall -Wextra -Werror -pedantic -O2 busflow.c -o busflow.exe
busflow.exe
```

The program stores its data file in the current working directory. Keep the data file if booking records need to persist between runs.

---

# 5. IMPLEMENTATION CODE

The complete implementation is maintained in the project source file:

**`busflow.c`**

For the final printed report, include the complete, current source listing from that file in this section or as an appendix. Do not substitute pseudocode or an older code copy. The source file is available in the project repository:

https://github.com/Davidunknown99/Bus-flow/blob/feat/busflow-booking-foundation/busflow.c

---

# 6. SAMPLE OUTPUT AND TESTING

The following is the demonstration sequence to execute during the laboratory evaluation. The exact PNR and seat availability depend on the local data file and each run.

1. Start the program and display the main menu.
2. Select **1 — Display all buses** to show the sample routes.
3. Select **2 — Search buses by route** and enter `Hyderabad` as origin and `Bengaluru` as destination.
4. Select **3 — View seat availability** and inspect the 24-seat layout.
5. Select **4 — Book a seat**, choose an available seat, and enter passenger details.
6. Record the generated PNR and displayed confirmation.
7. Select **5 — Find booking using PNR** and enter the generated PNR.
8. Select **7 — View booking history** to display the active booking.
9. Select **6 — Cancel a booking**, enter the PNR and the same mobile number, and confirm cancellation.
10. View the seat map again to verify that the cancelled seat is available.

## 6.1 Sample route data

| Operator | Route | Departure | Arrival | Sample fare |
|---|---|---:|---:|---:|
| Metro Travels | Hyderabad – Bengaluru | 21:00 | 06:00 | ₹1,499 |
| Orange Express | Hyderabad – Vijayawada | 07:00 | 13:00 | ₹799 |
| Kaveri Lines | Hyderabad – Chennai | 22:00 | 08:00 | ₹1,299 |
| Deccan Roadways | Hyderabad – Warangal | 08:30 | 11:30 | ₹399 |

## 6.2 Test cases

| Test | Action | Expected result |
|---|---|---|
| Route search | Search Hyderabad to Bengaluru | Matching sample route is displayed |
| Invalid route | Search a route not in sample data | No matching bus is displayed |
| Seat map | Open a bus seat map | 24 seats are displayed |
| Booking | Select an available seat and enter passenger details | PNR and confirmation are displayed |
| Duplicate seat | Attempt to book an occupied seat | Booking is not accepted |
| PNR lookup | Enter an active PNR | Matching booking details are displayed |
| Cancellation | Enter PNR and matching mobile number | Booking is cancelled |
| Persistence | Restart after saving a booking | Saved booking records are loaded |

> **Evidence to add before submission:** Insert clear screenshots or photographs of (a) the main menu, (b) bus search results, (c) seat map, (d) successful booking confirmation, (e) PNR lookup, and (f) cancellation / updated seat map. Capture these from an actual run of the final source code.

---

# 7. CONCLUSION

BusFlow demonstrates the implementation of a basic reservation workflow using the C programming language. It applies structures, arrays, functions, loops, conditional statements, string handling, and file operations to a practical problem. The project provides a compact example of how modular C programming can be used to manage route information and booking records in a local console application.

The current version is an academic prototype. Future improvements could include administrator-managed routes, date-wise schedules, stronger record validation, and a database-backed multi-user system.

---

# REFERENCES

1. ISO/IEC 9899:2011, *Programming Languages — C* (C11 language standard).
2. GCC Documentation, *Using the GNU Compiler Collection*, https://gcc.gnu.org/onlinedocs/
3. cppreference.com, *C language reference*, https://en.cppreference.com/w/c
4. B. V. Raju Institute of Technology, Computer Programming and Data Structures Laboratory course material, where applicable.
