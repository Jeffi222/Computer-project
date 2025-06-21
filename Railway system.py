import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        mycon = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="Railway_mgmt"
        )
        if mycon.is_connected():
            print("✅ Connected to Railway_mgmt")
            return mycon
    except Error as e:
        print("❌ Connection failed:", e)
        return None

def view_trains(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM trains")
    for row in cursor.fetchall():
        print(row)

def view_passengers(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM passenger")
    for row in cursor.fetchall():
        print(row)

def view_reservations(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM reservations")  
    for row in cursor.fetchall():
        print(row)

def book_ticket(con):
    try:
        cursor = con.cursor()

        print("\n--- Enter Passenger Details ---")
        name = input("Name: ")
        age = int(input("Age: "))
        gender = input("Gender (M/F): ")
        phone_number = int(input("Phone Number: "))

        cursor.execute(
            "INSERT INTO passenger (name, age, gender, phone_number) VALUES (%s, %s, %s, %s)",
            (name, age, gender, phone_number)
        )
        con.commit()

        pid = cursor.lastrowid
        print(f"✅ Passenger added with ID: {pid}")

        cursor.execute("SELECT train_id, train_name FROM trains")
        print("\nAvailable Trains:")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Train: {row[1]}")

        tid = int(input("Enter Train ID: "))
        date = input("Enter Date of Journey (YYYY-MM-DD): ")
        seat = input("Enter Seat Number (e.g., A1-23): ")

        check_query = """
            SELECT * FROM reservations
            WHERE train_id = %s AND travel_date = %s AND seat_number = %s
        """
        cursor.execute(check_query, (tid, date, seat))
        existing = cursor.fetchone()

        if existing:
            status = "Waiting"
            print("⚠️ Seat already booked! Your status is set to Waiting.")
        else:
            status = "Confirmed"

        query = """
            INSERT INTO reservations (passenger_id, train_id, travel_date, seat_number, booking_status)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (pid, tid, date, seat, status))
        con.commit()
        print(f"✅ Ticket booked successfully with status: {status}")

    except Exception as e:
        print("❌ Booking failed:", e)

def main():
    con = connect_db()
    if not con:
        return

    while True:
        print("\n=== Railway Management System ===")
        print("1. View Trains")
        print("2. View Passengers")
        print("3. View Reservations")
        print("4. Book a Ticket")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_trains(con)
        elif choice == "2":
            view_passengers(con)
        elif choice == "3":
            view_reservations(con)
        elif choice == "4":
            book_ticket(con)    
        elif choice == "5":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")

    con.close()

if __name__ == "__main__":
    main()
