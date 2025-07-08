import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import os

def connect_db():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="Railway_mgmt"
        )
        return con
    except mysql.connector.Error:
        messagebox.showerror("Database Error", "Failed to connect to MySQL.")
        return None

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def load_logo(frame):
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        img = Image.open(logo_path)
        img = img.resize((180, 180))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(frame, image=logo, bg="#990000")
        logo_label.image = logo
        logo_label.pack(pady=10)
    except Exception as e:
        print("❌ Logo could not be loaded:", e)

def main_menu(root, frame, con):
    clear_frame(frame)
    frame.configure(bg="#990000")

    tk.Label(frame, text="RAILWAY MANAGEMENT", font=("Arial", 28, "bold"), fg="white", bg="#990000").pack(pady=20)
    load_logo(frame)

    buttons = [
        ("View Trains", lambda: view_trains(frame, con)),
        ("View Passengers", lambda: view_passengers(frame, con)),
        ("View Reservations", lambda: view_reservations(frame, con)),
        ("Book Ticket", lambda: book_ticket(frame, con)),
        ("Exit", root.destroy)
    ]

    for text, cmd in buttons:
        tk.Button(frame, text=text, font=("Helvetica", 14), width=20, bg="#004080", fg="white", command=cmd).pack(pady=8)

def view_trains(frame, con):
    clear_frame(frame)
    tk.Label(frame, text="Train List", font=("Arial", 22, "bold"), bg="#990000", fg="white").pack(pady=15)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Source", "Destination", "Coach"), show="headings", height=10)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack()

    cursor = con.cursor()
    cursor.execute("SELECT train_id, train_name, source, destination, coach_type FROM trains")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    tk.Button(frame, text="Go Back", command=lambda: main_menu(root, frame, con), bg="#004080", fg="white", font=("Arial", 12)).pack(pady=15)

def view_passengers(frame, con):
    clear_frame(frame)
    tk.Label(frame, text="Passenger List", font=("Arial", 22, "bold"), bg="#990000", fg="white").pack(pady=15)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Age", "Gender", "Phone"), show="headings", height=10)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")
    tree.pack()

    cursor = con.cursor()
    cursor.execute("SELECT passenger_id, name, age, gender, phone_number FROM passenger")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    tk.Button(frame, text="Go Back", command=lambda: main_menu(root, frame, con), bg="#004080", fg="white", font=("Arial", 12)).pack(pady=15)

def view_reservations(frame, con):
    clear_frame(frame)
    tk.Label(frame, text="Reservation List", font=("Arial", 22, "bold"), bg="#990000", fg="white").pack(pady=15)

    tree = ttk.Treeview(frame, columns=("RID", "Passenger ID", "Train ID", "Date", "Seat", "Status"), show="headings", height=10)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack()

    cursor = con.cursor()
    cursor.execute("SELECT reservation_id, passenger_id, train_id, travel_date, seat_number, booking_status FROM reservations")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    tk.Button(frame, text="Go Back", command=lambda: main_menu(root, frame, con), bg="#004080", fg="white", font=("Arial", 12)).pack(pady=15)

def book_ticket(frame, con):
    clear_frame(frame)
    tk.Label(frame, text="Book Ticket", font=("Arial", 22, "bold"), bg="#990000", fg="white").pack(pady=10)

    fields = {}
    for label_text in ["Name", "Age", "Gender", "Phone Number", "Travel Date (YYYY-MM-DD)", "Seat Number"]:
        tk.Label(frame, text=label_text, font=("Arial", 12), bg="#990000", fg="white").pack()
        entry = tk.Entry(frame, font=("Arial", 12), width=25)
        entry.pack(pady=5)
        fields[label_text] = entry

    tk.Label(frame, text="Select Train", font=("Arial", 12), bg="#990000", fg="white").pack()
    train_combo = ttk.Combobox(frame, font=("Arial", 12), width=30)
    train_combo.pack(pady=5)

    cursor = con.cursor()
    cursor.execute("SELECT train_id, train_name, source, destination, coach_type FROM trains")
    train_data = cursor.fetchall()
    train_combo['values'] = [f"{tid} - {name} ({src} to {dst}) [{coach}]" for tid, name, src, dst, coach in train_data]

    def submit():
        name = fields["Name"].get()
        age = fields["Age"].get()
        gender = fields["Gender"].get()
        phone = fields["Phone Number"].get()
        date = fields["Travel Date (YYYY-MM-DD)"].get()
        seat = fields["Seat Number"].get()
        selected_train = train_combo.get()

        if not selected_train or not all([name, age, gender, phone, date, seat]):
            messagebox.showwarning("Incomplete", "Fill all fields.")
            return

        train_id = int(selected_train.split(" - ")[0])
        cursor.execute("INSERT INTO passenger (name, age, gender, phone_number) VALUES (%s, %s, %s, %s)", (name, age, gender, phone))
        con.commit()
        pid = cursor.lastrowid

        cursor.execute("SELECT * FROM reservations WHERE train_id=%s AND travel_date=%s AND seat_number=%s", (train_id, date, seat))
        exists = cursor.fetchone()
        status = "Waiting" if exists else "Confirmed"

        cursor.execute("INSERT INTO reservations (passenger_id, train_id, travel_date, seat_number, booking_status) VALUES (%s, %s, %s, %s, %s)", (pid, train_id, date, seat, status))
        con.commit()
        messagebox.showinfo("Done", f"Ticket booked with status: {status}")

    tk.Button(frame, text="Submit", command=submit, font=("Arial", 12), bg="#004080", fg="white").pack(pady=10)
    tk.Button(frame, text="Go Back", command=lambda: main_menu(root, frame, con), font=("Arial", 12), bg="#004080", fg="white").pack()

def launch_gui():
    global root
    root = tk.Tk()
    root.title("Railway Management System")
    root.configure(bg="#990000")
    root.state("zoomed")

    con = connect_db()
    if not con:
        return

    main_frame = tk.Frame(root, bg="#990000")
    main_frame.pack(fill="both", expand=True)

    main_menu(root, main_frame, con)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
