import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
import datetime

# MySQL Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="Railway_mgmt"
    )

# App
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Railway Management System")
app.attributes("-fullscreen", True)
app.configure(fg_color="black")

current_frame = None

def clear_frame():
    global current_frame
    if current_frame:
        current_frame.destroy()

def go_back(to_func):
    clear_frame()
    to_func()

def logout():
    app.destroy()

def main_menu():
    global current_frame
    clear_frame()
    current_frame = ctk.CTkFrame(app, fg_color="black")
    current_frame.pack(expand=True)

    title = ctk.CTkLabel(current_frame, text="Railway Management System", font=("Arial", 36), text_color="white")
    title.pack(pady=40)

    admin_btn = ctk.CTkButton(current_frame, text="Admin Login", corner_radius=20, width=250, height=60, command=admin_login_screen)
    admin_btn.pack(pady=20)

    user_btn = ctk.CTkButton(current_frame, text="User / Customer", corner_radius=20, width=250, height=60, command=user_menu)
    user_btn.pack(pady=20)

    logout_btn = ctk.CTkButton(current_frame, text="Exit App", fg_color="red", hover_color="#aa0000", corner_radius=20, width=250, height=60, command=logout)
    logout_btn.pack(pady=40)

def admin_login_screen():
    global current_frame
    clear_frame()
    current_frame = ctk.CTkFrame(app, fg_color="black")
    current_frame.pack(expand=True)

    title = ctk.CTkLabel(current_frame, text="Admin Login", font=("Arial", 28), text_color="white")
    title.pack(pady=20)

    username_label = ctk.CTkLabel(current_frame, text="Username", text_color="white")
    username_label.pack()
    username = ctk.CTkEntry(current_frame, width=250)
    username.pack(pady=10)

    password_label = ctk.CTkLabel(current_frame, text="Password", text_color="white")
    password_label.pack()
    password = ctk.CTkEntry(current_frame, show="*", width=250)
    password.pack(pady=10)

    def check_login():
        user = username.get()
        pwd = password.get()
        if user.lower() in ["jeffi", "nidhin", "eldho"] and pwd == "1234":
            admin_menu()
        else:
            messagebox.showerror("Access Denied", "Invalid credentials!")

    login_btn = ctk.CTkButton(current_frame, text="Login", corner_radius=20, command=check_login)
    login_btn.pack(pady=20)

    back_btn = ctk.CTkButton(current_frame, text="Back", corner_radius=20, command=lambda: go_back(main_menu))
    back_btn.pack()

def admin_menu():
    global current_frame
    clear_frame()
    current_frame = ctk.CTkFrame(app, fg_color="black")
    current_frame.pack(expand=True)

    title = ctk.CTkLabel(current_frame, text="Admin Dashboard", font=("Arial", 30), text_color="white")
    title.pack(pady=20)

    options = [
        ("Add Train", add_train),
        ("Update Train", update_train),
        ("Delete Train", delete_train),
        ("View All Trains", view_trains),
        ("View Passengers", view_passengers),
        ("Delete Passenger", delete_passenger),
        ("View Reservations", view_reservations),
        ("Cancel Reservation", cancel_reservation),
        ("Logout", main_menu)
    ]

    for name, func in options:
        btn_color = "red" if name == "Logout" else "#1f538d"
        btn = ctk.CTkButton(current_frame, text=name, command=func, width=250, height=50, corner_radius=20, fg_color=btn_color)
        btn.pack(pady=8)

# ---- ADMIN FUNCTIONS ----
def add_train():
    clear_frame()
    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(expand=True)

    ctk.CTkLabel(frame, text="Add Train", font=("Arial", 24), text_color="white").pack(pady=10)

    tname = ctk.CTkEntry(frame, placeholder_text="Train Name", width=250)
    tname.pack(pady=5)

    src = ctk.CTkEntry(frame, placeholder_text="Source", width=250)
    src.pack(pady=5)

    dest = ctk.CTkEntry(frame, placeholder_text="Destination", width=250)
    dest.pack(pady=5)

    coach = ctk.CTkEntry(frame, placeholder_text="Coach Type", width=250)
    coach.pack(pady=5)

    def insert_train():
        con = connect_db()
        cur = con.cursor()
        cur.execute("INSERT INTO trains (train_name, source, destination, coach_type) VALUES (%s, %s, %s, %s)",
                    (tname.get(), src.get(), dest.get(), coach.get()))
        con.commit()
        messagebox.showinfo("Success", "Train added successfully!")
        go_back(admin_menu)

    ctk.CTkButton(frame, text="Add", command=insert_train).pack(pady=10)
    ctk.CTkButton(frame, text="Go Back", command=lambda: go_back(admin_menu)).pack()

def update_train():
    clear_frame()
    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(expand=True)

    ctk.CTkLabel(frame, text="Update Train", font=("Arial", 24), text_color="white").pack(pady=10)

    tid = ctk.CTkEntry(frame, placeholder_text="Train ID", width=250)
    tid.pack(pady=5)

    new_name = ctk.CTkEntry(frame, placeholder_text="New Train Name", width=250)
    new_name.pack(pady=5)

    def do_update():
        con = connect_db()
        cur = con.cursor()
        cur.execute("UPDATE trains SET train_name=%s WHERE train_id=%s", (new_name.get(), tid.get()))
        con.commit()
        messagebox.showinfo("Updated", "Train name updated.")
        go_back(admin_menu)

    ctk.CTkButton(frame, text="Update", command=do_update).pack(pady=10)
    ctk.CTkButton(frame, text="Go Back", command=lambda: go_back(admin_menu)).pack()

def delete_train():
    clear_frame()
    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(expand=True)

    ctk.CTkLabel(frame, text="Delete Train", font=("Arial", 24), text_color="white").pack(pady=10)

    tid = ctk.CTkEntry(frame, placeholder_text="Train ID", width=250)
    tid.pack(pady=5)

    def do_delete():
        con = connect_db()
        cur = con.cursor()
        cur.execute("DELETE FROM trains WHERE train_id=%s", (tid.get(),))
        con.commit()
        messagebox.showinfo("Deleted", "Train deleted.")
        go_back(admin_menu)

    ctk.CTkButton(frame, text="Delete", command=do_delete).pack(pady=10)
    ctk.CTkButton(frame, text="Go Back", command=lambda: go_back(admin_menu)).pack()

def view_trains():
    show_table("SELECT * FROM trains", ["ID", "Name", "From", "To", "Coach"], admin_menu)

def view_passengers():
    show_table("SELECT * FROM passenger", ["ID", "Name", "Age", "Gender", "Phone"], admin_menu)

def delete_passenger():
    delete_generic("passenger", "passenger_id", admin_menu)

def view_reservations():
    show_table("SELECT * FROM reservations", ["ID", "Passenger ID", "Train ID", "Date", "Seat", "Status"], admin_menu)

def cancel_reservation():
    delete_generic("reservations", "reservation_id", admin_menu)

def delete_generic(table, col, back_func):
    clear_frame()
    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(expand=True)

    ctk.CTkLabel(frame, text=f"Delete from {table}", font=("Arial", 24), text_color="white").pack(pady=10)

    eid = ctk.CTkEntry(frame, placeholder_text=f"{col.replace('_', ' ').title()}", width=250)
    eid.pack(pady=5)

    def do_delete():
        con = connect_db()
        cur = con.cursor()
        cur.execute(f"DELETE FROM {table} WHERE {col}=%s", (eid.get(),))
        con.commit()
        messagebox.showinfo("Deleted", f"Deleted from {table}")
        go_back(back_func)

    ctk.CTkButton(frame, text="Delete", command=do_delete).pack(pady=10)
    ctk.CTkButton(frame, text="Go Back", command=lambda: go_back(back_func)).pack()

# USER
def user_menu():
    global current_frame
    clear_frame()
    current_frame = ctk.CTkFrame(app, fg_color="black")
    current_frame.pack(expand=True)

    ctk.CTkLabel(current_frame, text="Welcome, Passenger", font=("Arial", 26), text_color="white").pack(pady=30)

    ctk.CTkButton(current_frame, text="Book Ticket", command=book_ticket).pack(pady=10)
    ctk.CTkButton(current_frame, text="View My Reservation", command=view_user_reservation).pack(pady=10)
    ctk.CTkButton(current_frame, text="Go Back", command=lambda: go_back(main_menu)).pack(pady=10)

def book_ticket():
    clear_frame()
    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(expand=True)

    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT train_id, train_name, source, destination FROM trains")
    trains = cur.fetchall()

    train_map = {f"{t[1]} ({t[2]} ➜ {t[3]})": t[0] for t in trains}
    options = list(train_map.keys())

    ctk.CTkLabel(frame, text="Book Ticket", font=("Arial", 24), text_color="white").pack(pady=10)

    name = ctk.CTkEntry(frame, placeholder_text="Name", width=250)
    name.pack(pady=5)

    age = ctk.CTkEntry(frame, placeholder_text="Age", width=250)
    age.pack(pady=5)

    gender = ctk.CTkEntry(frame, placeholder_text="Gender", width=250)
    gender.pack(pady=5)

    phone = ctk.CTkEntry(frame, placeholder_text="Phone Number", width=250)
    phone.pack(pady=5)

    dropdown = ctk.CTkOptionMenu(frame, values=options)
    dropdown.pack(pady=5)

    date = ctk.CTkEntry(frame, placeholder_text="YYYY-MM-DD", width=250)
    date.pack(pady=5)

    seat = ctk.CTkEntry(frame, placeholder_text="Seat Number (e.g., A1-23)", width=250)
    seat.pack(pady=5)

    def confirm_booking():
        train_id = train_map[dropdown.get()]
        cur.execute("INSERT INTO passenger (name, age, gender, phone_number) VALUES (%s, %s, %s, %s)",
                    (name.get(), age.get(), gender.get(), phone.get()))
        con.commit()
        pid = cur.lastrowid

        cur.execute("SELECT * FROM reservations WHERE train_id=%s AND travel_date=%s AND seat_number=%s",
                    (train_id, date.get(), seat.get()))
        existing = cur.fetchone()
        status = "Waiting" if existing else "Confirmed"

        cur.execute("INSERT INTO reservations (passenger_id, train_id, travel_date, seat_number, booking_status) VALUES (%s,%s,%s,%s,%s)",
                    (pid, train_id, date.get(), seat.get(), status))
        con.commit()

        messagebox.showinfo("Success", f"Ticket booked!\nPassenger ID: {pid}")
        go_back(user_menu)

    ctk.CTkButton(frame, text="Confirm Booking", command=confirm_booking).pack(pady=10)
    ctk.CTkButton(frame, text="Go Back", command=lambda: go_back(user_menu)).pack()

def view_user_reservation():
    clear_frame()
    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(expand=True)

    ctk.CTkLabel(frame, text="View Your Reservation", font=("Arial", 24), text_color="white").pack(pady=10)
    pid = ctk.CTkEntry(frame, placeholder_text="Enter Your Passenger ID", width=250)
    pid.pack(pady=5)

    def fetch():
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM reservations WHERE passenger_id=%s", (pid.get(),))
        rows = cur.fetchall()

        show_table_data(rows, ["ID", "Passenger ID", "Train ID", "Date", "Seat", "Status"], user_menu)

    ctk.CTkButton(frame, text="View", command=fetch).pack(pady=10)
    ctk.CTkButton(frame, text="Go Back", command=lambda: go_back(user_menu)).pack()

def show_table(query, cols, back_func):
    clear_frame()
    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(expand=True)

    con = connect_db()
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    show_table_data(rows, cols, back_func)

def show_table_data(rows, cols, back_func):
    table = ttk.Treeview(current_frame, columns=cols, show="headings", height=15)
    for col in cols:
        table.heading(col, text=col)
        table.column(col, width=100)
    for row in rows:
        table.insert("", "end", values=row)
    table.pack(pady=10)
    ctk.CTkButton(current_frame, text="Go Back", command=lambda: go_back(back_func)).pack(pady=20)

# Start the app
main_menu()
app.mainloop()
