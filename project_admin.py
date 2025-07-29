import mysql.connector as mc
def connection():
    mycon=mc.connect(host='localhost',user='root',passwd='***',database='railway_mgmt')
    
print('----------WELCOME----------')



def admin_user():
    
    a=input('ADMIN/USER- if you are an admin press A / if you are a customer press C- ')
    if a=='A':
        passwd='ABCD'
        b=input('ENTER THE PASSWORD-')
        if b==passwd:
            print('LOGIN SUCCESSFULL')
        else:
            print('incorrect password')

    elif a=='C':
        print('welcome')
admin_user()



def add_train(mycon):
    train_id = input("Enter Train ID: ")
    name = input("Enter Train Name: ")
    source = input("Enter Source Station: ")
    dest = input("Enter Destination Station: ")
    coach = input("Enter Coach Type: ")

    cursor = mycon.cursor()
    try:
        cursor.execute("INSERT INTO trains VALUES (%s, %s, %s, %s, %s)", (train_id, name, source, dest, coach))
        con.commit()
        print("✅ Train added successfully.\n")
    except Exception as e:
        print("❌ Error:", e)

def update_train(mycon):
    train_id = input("Enter Train ID to update: ")
    name = input("New Train Name: ")
    source = input("New Source: ")
    dest = input("New Destination: ")
    coach = input("New Coach Type: ")

    cursor = mycon.cursor()
    try:
        cursor.execute("UPDATE trains SET train_name=%s, source=%s, destination=%s, coach_type=%s WHERE train_id=%s",
                       (name, source, dest, coach, train_id))
        mycon.commit()
        print("✅ Train updated.\n")
    except Exception as e:
        print("❌ Error:", e)

def delete_train(mycon):
    train_id = input("Enter Train ID to delete: ")
    cursor = mycon.cursor()
    try:
        cursor.execute("DELETE FROM trains WHERE train_id=%s", (train_id,))
        mycon.commit()
        print("✅ Train deleted.\n")
    except Exception as e:
        print("❌ Error:", e)

def view_trains(mycon):
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM trains")
    rows = cursor.fetchall()
    print("\n🚆 Train List:")
    print("{:<10} {:<20} {:<15} {:<15} {:<10}".format("ID", "Name", "Source", "Dest", "Coach"))
    for row in rows:
        print("{:<10} {:<20} {:<15} {:<15} {:<10}".format(*row))
    print()

def view_passengers(mycon):
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM passenger")
    rows = cursor.fetchall()
    print("\n👤 Passenger List:")
    print("{:<5} {:<20} {:<5} {:<10} {:<15}".format("ID", "Name", "Age", "Gender", "Phone"))
    for row in rows:
        print("{:<5} {:<20} {:<5} {:<10} {:<15}".format(*row))
    print()

def delete_passenger(mycon):
    pid = input("Enter Passenger ID to delete: ")
    cursor = mycon.cursor()
    try:
        cursor.execute("DELETE FROM passenger WHERE passenger_id=%s", (pid,))
        mycon.commit()
        print("✅ Passenger deleted.\n")
    except Exception as e:
        print("❌ Error:", e)

def view_reservations(con):
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()
    print("\n🧾 Reservations List:")
    print("{:<5} {:<5} {:<5} {:<12} {:<10} {:<10}".format("RID", "PID", "TID", "Date", "Seat", "Status"))
    for row in rows:
        print("{:<5} {:<5} {:<5} {:<12} {:<10} {:<10}".format(*row))
    print()

def delete_reservation(mycon):
    rid = input("Enter Reservation ID to delete: ")
    cursor = mycon.cursor()
    try:
        cursor.execute("DELETE FROM reservations WHERE reservation_id=%s", (rid,))
        mycon.commit()
        print("✅ Reservation cancelled.\n")
    except Exception as e:
        print("❌ Error:", e)

def admin_menu(mycon):
    while True:
        print("""
======= ADMIN MENU =======
1. Add Train
2. Update Train
3. Delete Train
4. View All Trains
5. View Passengers
6. Delete Passenger
7. View Reservations
8. Cancel Reservation
9. Exit
""")
        choice = input("Enter choice: ")

        if choice == "1":
            add_train(con)
        elif choice == "2":
            update_train(con)
        elif choice == "3":
            delete_train(con)
        elif choice == "4":
            view_trains(con)
        elif choice == "5":
            view_passengers(con)
        elif choice == "6":
            delete_passenger(con)
        elif choice == "7":
            view_reservations(con)
        elif choice == "8":
            delete_reservation(con)
        elif choice == "9":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        mycon = connect_db()
        admin_menu(mycon)
        mycon.close()
    except Exception as e:
        print("❌ Could not connect to database:", e)
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="Railway_mgmt"
    )

def add_train(con):
    train_id = input("Enter Train ID: ")
    name = input("Enter Train Name: ")
    source = input("Enter Source Station: ")
    dest = input("Enter Destination Station: ")
    coach = input("Enter Coach Type: ")

    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO trains VALUES (%s, %s, %s, %s, %s)", (train_id, name, source, dest, coach))
        con.commit()
        print("✅ Train added successfully.\n")
    except Exception as e:
        print("❌ Error:", e)