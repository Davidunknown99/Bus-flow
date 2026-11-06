/*
 * BusFlow - C11 Console Bus Booking Demo
 * Build: gcc -std=c11 -Wall -Wextra -pedantic -O2 busflow.c -o busflow
 */
#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BUS_COUNT 4
#define SEATS_PER_BUS 24
#define MAX_BOOKINGS 500
#define NAME_LEN 80
#define PHONE_LEN 20
#define PNR_LEN 20
#define DATA_FILE "busflow_bookings.dat"

typedef struct {
    int id;
    char operator_name[40];
    char bus_name[40];
    char origin[32];
    char destination[32];
    char departure[8];
    char arrival[8];
    int fare;
} Bus;

typedef struct {
    int active;
    char pnr[PNR_LEN];
    int bus_id;
    int seat_number;
    char passenger[NAME_LEN];
    char phone[PHONE_LEN];
    int fare;
} Booking;

static const Bus buses[BUS_COUNT] = {
    {1, "Metro Travels", "Volvo AC Sleeper", "Hyderabad", "Bengaluru", "21:00", "06:00", 1499},
    {2, "Orange Express", "AC Semi Sleeper", "Hyderabad", "Vijayawada", "07:00", "13:00", 799},
    {3, "Kaveri Lines", "BharatBenz Sleeper", "Hyderabad", "Chennai", "22:00", "08:00", 1299},
    {4, "Deccan Roadways", "AC Seater", "Hyderabad", "Warangal", "08:30", "11:30", 399}
};

static Booking bookings[MAX_BOOKINGS];
static int booking_count = 0;

static void trim_newline(char *s) {
    size_t n = strlen(s);
    while (n > 0 && (s[n - 1] == '\n' || s[n - 1] == '\r')) {
        s[--n] = '\0';
    }
}

static void read_text(const char *prompt, char *out, size_t size) {
    for (;;) {
        printf("%s", prompt);
        if (!fgets(out, (int)size, stdin)) {
            out[0] = '\0';
            return;
        }
        trim_newline(out);
        if (out[0] != '\0') return;
        puts("Please enter a value.");
    }
}

static int read_int(const char *prompt, int min, int max) {
    char line[64], *end;
    long value;
    for (;;) {
        printf("%s", prompt);
        if (!fgets(line, sizeof line, stdin)) return min;
        errno = 0;
        value = strtol(line, &end, 10);
        while (*end && isspace((unsigned char)*end)) end++;
        if (errno == 0 && end != line && *end == '\0' && value >= min && value <= max)
            return (int)value;
        printf("Enter a number from %d to %d.\n", min, max);
    }
}

static void pause_screen(void) {
    char line[8];
    printf("\nPress Enter to continue...");
    (void)fgets(line, sizeof line, stdin);
}

static int equals_ignore_case(const char *a, const char *b) {
    while (*a && *b) {
        if (tolower((unsigned char)*a) != tolower((unsigned char)*b)) return 0;
        a++; b++;
    }
    return *a == '\0' && *b == '\0';
}

static int bus_index(int id) {
    int i;
    for (i = 0; i < BUS_COUNT; i++) if (buses[i].id == id) return i;
    return -1;
}

static int seat_is_booked(int bus_id, int seat_no) {
    int i;
    for (i = 0; i < booking_count; i++) {
        if (bookings[i].active && bookings[i].bus_id == bus_id &&
            bookings[i].seat_number == seat_no) return 1;
    }
    return 0;
}

static void load_bookings(void) {
    FILE *file = fopen(DATA_FILE, "rb");
    if (!file) return;
    while (booking_count < MAX_BOOKINGS &&
           fread(&bookings[booking_count], sizeof(Booking), 1, file) == 1) {
        booking_count++;
    }
    fclose(file);
}

static int save_bookings(void) {
    FILE *file = fopen(DATA_FILE, "wb");
    if (!file) {
        perror("Could not save bookings");
        return 0;
    }
    if (booking_count > 0 &&
        fwrite(bookings, sizeof(Booking), (size_t)booking_count, file) != (size_t)booking_count) {
        perror("Could not write bookings");
        fclose(file);
        return 0;
    }
    fclose(file);
    return 1;
}

static void print_header(void) {
    puts("\n==============================================================");
    puts("                         BUSFLOW");
    puts("                 SIMPLE BUS BOOKING DEMO");
    puts("==============================================================");
}

static void show_buses(void) {
    int i;
    puts("\nAVAILABLE BUSES");
    puts("--------------------------------------------------------------------------------");
    printf("%-3s %-18s %-20s %-12s %-12s %-7s %-7s %s\n",
           "ID", "OPERATOR", "BUS", "FROM", "TO", "DEPART", "ARRIVE", "FARE");
    puts("--------------------------------------------------------------------------------");
    for (i = 0; i < BUS_COUNT; i++) {
        printf("%-3d %-18s %-20s %-12s %-12s %-7s %-7s Rs.%d\n",
               buses[i].id, buses[i].operator_name, buses[i].bus_name,
               buses[i].origin, buses[i].destination, buses[i].departure,
               buses[i].arrival, buses[i].fare);
    }
}

static void search_buses(void) {
    char origin[32], destination[32];
    int i, matches = 0;
    read_text("\nEnter source city: ", origin, sizeof origin);
    read_text("Enter destination city: ", destination, sizeof destination);
    puts("\nMATCHING BUSES");
    for (i = 0; i < BUS_COUNT; i++) {
        if (equals_ignore_case(origin, buses[i].origin) &&
            equals_ignore_case(destination, buses[i].destination)) {
            printf("%d. %s | %s | %s to %s | %s - %s | Rs.%d\n",
                   buses[i].id, buses[i].operator_name, buses[i].bus_name,
                   buses[i].origin, buses[i].destination, buses[i].departure,
                   buses[i].arrival, buses[i].fare);
            matches++;
        }
    }
    if (!matches) puts("No buses found for that route. Try the available routes.");
}

static void show_seats(int bus_id) {
    int seat;
    puts("\n                 FRONT / DRIVER");
    puts("              -------------------");
    puts("       LEFT SIDE       AISLE       RIGHT SIDE");
    for (seat = 1; seat <= SEATS_PER_BUS; seat += 4) {
        int a = seat, b = seat + 1, c = seat + 2, d = seat + 3;
        printf("       [%02d]%s [%02d]       ||       [%02d]%s [%02d]\n",
               a, seat_is_booked(bus_id, a) ? "X" : " ",
               b, seat_is_booked(bus_id, b) ? "X" : " ",
               c, seat_is_booked(bus_id, c) ? "X" : " ",
               d, seat_is_booked(bus_id, d) ? "X" : " ");
    }
    puts("X = booked; blank = available");
}

static void make_pnr(char *out, size_t size) {
    unsigned long stamp = (unsigned long)time(NULL);
    unsigned long serial = (unsigned long)booking_count + 1UL;
    (void)snprintf(out, size, "BF%06lu", (stamp + serial * 37UL) % 1000000UL);
}

static void book_seat(void) {
    int id, idx, seat, available = 0, i;
    char passenger[NAME_LEN], phone[PHONE_LEN];
    Booking b;
    if (booking_count >= MAX_BOOKINGS) {
        puts("Booking storage is full for this demo.");
        return;
    }
    show_buses();
    id = read_int("\nEnter bus ID (0 to go back): ", 0, BUS_COUNT);
    if (id == 0) return;
    idx = bus_index(id);
    if (idx < 0) return;
    show_seats(id);
    for (i = 1; i <= SEATS_PER_BUS; i++) if (!seat_is_booked(id, i)) available++;
    if (!available) {
        puts("Sorry, this bus is fully booked.");
        return;
    }
    printf("\nAvailable seats: %d\n", available);
    seat = read_int("Choose seat number: ", 1, SEATS_PER_BUS);
    if (seat_is_booked(id, seat)) {
        puts("That seat is already booked. Please choose another seat.");
        return;
    }
    read_text("Passenger full name: ", passenger, sizeof passenger);
    read_text("Mobile number: ", phone, sizeof phone);
    memset(&b, 0, sizeof b);
    b.active = 1;
    b.bus_id = id;
    b.seat_number = seat;
    b.fare = buses[idx].fare;
    (void)snprintf(b.passenger, sizeof b.passenger, "%s", passenger);
    (void)snprintf(b.phone, sizeof b.phone, "%s", phone);
    make_pnr(b.pnr, sizeof b.pnr);
    bookings[booking_count++] = b;
    if (!save_bookings()) {
        booking_count--;
        puts("Booking was not saved. Please try again.");
        return;
    }
    puts("\n---------------- BOOKING CONFIRMED ----------------");
    printf("PNR          : %s\n", b.pnr);
    printf("Passenger    : %s\n", b.passenger);
    printf("Route        : %s to %s\n", buses[idx].origin, buses[idx].destination);
    printf("Bus          : %s (%s)\n", buses[idx].operator_name, buses[idx].bus_name);
    printf("Departure    : %s\n", buses[idx].departure);
    printf("Seat         : %02d\n", b.seat_number);
    printf("Ticket fare  : Rs.%d\n", b.fare);
    puts("---------------------------------------------------");
    puts("Demo booking only. No payment or real ticket is issued.");
}

static int find_booking(const char *pnr) {
    int i;
    for (i = 0; i < booking_count; i++) {
        if (bookings[i].active && strcmp(bookings[i].pnr, pnr) == 0) return i;
    }
    return -1;
}

static void find_booking_menu(void) {
    char pnr[PNR_LEN];
    int pos, idx;
    read_text("\nEnter PNR: ", pnr, sizeof pnr);
    pos = find_booking(pnr);
    if (pos < 0) {
        puts("Active booking not found.");
        return;
    }
    idx = bus_index(bookings[pos].bus_id);
    puts("\nBOOKING DETAILS");
    printf("PNR       : %s\n", bookings[pos].pnr);
    printf("Passenger : %s\n", bookings[pos].passenger);
    printf("Phone     : %s\n", bookings[pos].phone);
    if (idx >= 0) printf("Route     : %s to %s\n", buses[idx].origin, buses[idx].destination);
    printf("Seat      : %02d\n", bookings[pos].seat_number);
    printf("Fare      : Rs.%d\n", bookings[pos].fare);
    puts("Status    : CONFIRMED");
}

static void cancel_booking(void) {
    char pnr[PNR_LEN], phone[PHONE_LEN];
    int pos;
    read_text("\nEnter PNR to cancel: ", pnr, sizeof pnr);
    pos = find_booking(pnr);
    if (pos < 0) {
        puts("Active booking not found.");
        return;
    }
    read_text("Enter booking mobile number: ", phone, sizeof phone);
    if (strcmp(phone, bookings[pos].phone) != 0) {
        puts("Mobile number does not match. Cancellation denied.");
        return;
    }
    bookings[pos].active = 0;
    if (!save_bookings()) {
        bookings[pos].active = 1;
        puts("Cancellation could not be saved.");
        return;
    }
    printf("Booking %s cancelled. Seat %02d is available again.\n",
           bookings[pos].pnr, bookings[pos].seat_number);
}

static void booking_history(void) {
    int i, found = 0;
    puts("\nACTIVE BOOKING HISTORY");
    for (i = 0; i < booking_count; i++) {
        int idx;
        if (!bookings[i].active) continue;
        idx = bus_index(bookings[i].bus_id);
        printf("%s | %-18s | Seat %02d | Rs.%d",
               bookings[i].pnr, bookings[i].passenger,
               bookings[i].seat_number, bookings[i].fare);
        if (idx >= 0) printf(" | %s to %s", buses[idx].origin, buses[idx].destination);
        putchar('\n');
        found++;
    }
    if (!found) puts("No active bookings yet.");
}

static void show_seat_status(void) {
    int id;
    show_buses();
    id = read_int("\nEnter bus ID (0 to go back): ", 0, BUS_COUNT);
    if (id == 0) return;
    show_seats(id);
}

int main(void) {
    int choice;
    load_bookings();
    for (;;) {
        print_header();
        puts("  1. Display all buses");
        puts("  2. Search buses by route");
        puts("  3. View seat availability");
        puts("  4. Book a seat");
        puts("  5. Find booking using PNR");
        puts("  6. Cancel a booking");
        puts("  7. View booking history");
        puts("  0. Exit");
        choice = read_int("\nChoose an option: ", 0, 7);
        switch (choice) {
            case 1: show_buses(); pause_screen(); break;
            case 2: search_buses(); pause_screen(); break;
            case 3: show_seat_status(); pause_screen(); break;
            case 4: book_seat(); pause_screen(); break;
            case 5: find_booking_menu(); pause_screen(); break;
            case 6: cancel_booking(); pause_screen(); break;
            case 7: booking_history(); pause_screen(); break;
            case 0: puts("\nThank you for using BusFlow. Goodbye!"); return 0;
            default: break;
        }
    }
}