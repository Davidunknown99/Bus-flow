# BusFlow C11 Demo Guide

## 1. Compile

Linux/macOS:

~~~bash
gcc -std=c11 -Wall -Wextra -pedantic -O2 busflow.c -o busflow
./busflow
~~~

Windows with MinGW:

~~~bash
gcc -std=c11 -Wall -Wextra -pedantic -O2 busflow.c -o busflow.exe
busflow.exe
~~~

## 2. Demonstrate the application

1. Choose **1** to display all sample buses.
2. Choose **2** and search Hyderabad to Bengaluru.
3. Choose **3** to view the seat map for a bus. X marks a booked seat.
4. Choose **4**, select a bus and an available seat, then enter a passenger name and mobile number.
5. Show the generated PNR and booking confirmation.
6. Choose **5** and enter that PNR to retrieve the booking.
7. Choose **7** to show active booking history.
8. Choose **6** to cancel the booking using its PNR and the same mobile number.
9. Choose **3** again to show that the cancelled seat is available.

## 3. Persistence

Bookings are saved in busflow_bookings.dat in the current working directory. Exit and run the program again to demonstrate that active bookings remain saved.

## Academic demo notice

All routes and fares are sample data. No payment is processed and no real travel ticket is issued.
