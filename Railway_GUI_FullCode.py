import customtkinter as ctk
import mysql.connector
from tkinter import messagebox, simpledialog, ttk
import datetime
from tkcalendar import Calendar
from mysql.connector import errorcode

db_config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'Railway_mgmt'
}

def connect_db():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Failed to connect to database: {err}")
        return None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Railway Management System")
app.after(100, lambda: app.state('zoomed'))
app.configure(fg_color="black")

current_frame = None
current_passenger_id = None

def clear_frame():
    global current_frame
    if current_frame:
        for widget in current_frame.winfo_children():
            widget.destroy()
        current_frame.destroy()
    current_frame = None

def set_current_frame(frame_content_func):
    global current_frame
    clear_frame()

    frame = ctk.CTkFrame(app, fg_color="black")
    frame.pack(side="top", fill="both", expand=True, pady=0, padx=0)
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    frame_content_func(frame)
    
    current_frame = frame

def go_back(to_func):
    clear_frame()
    to_func()

def logout():
    app.destroy()

def main_menu():
    set_current_frame(lambda parent_frame: _create_main_menu_content(parent_frame))

def _create_main_menu_content(parent_frame):
    title = ctk.CTkLabel(parent_frame, text="Railway Management System", font=("Arial", 36), text_color="white")
    title.pack(pady=40)

    admin_btn = ctk.CTkButton(parent_frame, text="Admin Login", corner_radius=20, width=250, height=60, command=admin_login_screen)
    admin_btn.pack(pady=20)

    user_btn = ctk.CTkButton(parent_frame, text="User / Customer", corner_radius=20, width=250, height=60, command=user_menu)
    user_btn.pack(pady=20)

    logout_btn = ctk.CTkButton(parent_frame, text="Exit App", fg_color="red", hover_color="#aa0000", corner_radius=20, width=250, height=60, command=logout)
    logout_btn.pack(pady=40)

def admin_login_screen():
    set_current_frame(lambda parent_frame: _create_admin_login_content(parent_frame))

def _create_admin_login_content(parent_frame):
    title = ctk.CTkLabel(parent_frame, text="Admin Login", font=("Arial", 28), text_color="white")
    title.pack(pady=20)

    username_label = ctk.CTkLabel(parent_frame, text="Username", text_color="white")
    username_label.pack()
    username_entry = ctk.CTkEntry(parent_frame, width=250)
    username_entry.pack(pady=10)

    password_label = ctk.CTkLabel(parent_frame, text="Password", text_color="white")
    password_label.pack()
    password_entry = ctk.CTkEntry(parent_frame, show="*", width=250)
    password_entry.pack(pady=10)

    def check_login():
        user = username_entry.get()
        pwd = password_entry.get()
        if user.lower() in ["jeffi", "nidhin", "eldho"] and pwd == "1234":
            admin_menu()
        else:
            messagebox.showerror("Access Denied", "Invalid credentials!")

    login_btn = ctk.CTkButton(parent_frame, text="Login", corner_radius=20, command=check_login)
    login_btn.pack(pady=20)

    back_btn = ctk.CTkButton(parent_frame, text="Back", corner_radius=20, command=lambda: go_back(main_menu))
    back_btn.pack()

def admin_menu():
    set_current_frame(lambda parent_frame: _create_admin_menu_content(parent_frame))

def _create_admin_menu_content(parent_frame):
    title = ctk.CTkLabel(parent_frame, text="Admin Dashboard", font=("Arial", 30), text_color="white")
    title.pack(pady=20)

    options = [
        ("Add Train", add_train),
        ("Update Train", update_train),
        ("Delete Train", delete_train),
        ("Add/Update Bogie Capacity", add_bogie_capacity),
        ("View All Trains", view_trains),
        ("View Passengers", view_passengers),
        ("Delete Passenger", delete_passenger),
        ("View Reservations", view_reservations),
        ("Cancel Reservation", cancel_reservation_admin),
        ("Logout", main_menu)
    ]

    for name, func in options:
        btn_color = "red" if name == "Logout" else "#1f538d"
        btn = ctk.CTkButton(parent_frame, text=name, command=func, width=250, height=50, corner_radius=20, fg_color=btn_color)
        btn.pack(pady=8)

def add_train():
    set_current_frame(lambda parent_frame: _create_add_train_content(parent_frame))

def _create_add_train_content(parent_frame):
    ctk.CTkLabel(parent_frame, text="Add Train", font=("Arial", 24), text_color="white").pack(pady=10)

    tid_entry = ctk.CTkEntry(parent_frame, placeholder_text="Train ID (e.g., 101)", width=250)
    tid_entry.pack(pady=5)
    tname_entry = ctk.CTkEntry(parent_frame, placeholder_text="Train Name", width=250)
    tname_entry.pack(pady=5)
    src_entry = ctk.CTkEntry(parent_frame, placeholder_text="Source", width=250)
    src_entry.pack(pady=5)
    dest_entry = ctk.CTkEntry(parent_frame, placeholder_text="Destination", width=250)
    dest_entry.pack(pady=5)
    
    ctk.CTkLabel(parent_frame, text="Departure Time (HH:MM:SS):", text_color="white").pack(pady=(10, 0))
    dep_time_entry = ctk.CTkEntry(parent_frame, placeholder_text="e.g., 08:30:00", width=250)
    dep_time_entry.pack(pady=5)
    
    ctk.CTkLabel(parent_frame, text="Arrival Time (HH:MM:SS):", text_color="white").pack(pady=(10, 0))
    arr_time_entry = ctk.CTkEntry(parent_frame, placeholder_text="e.g., 18:00:00", width=250)
    arr_time_entry.pack(pady=5)

    def insert_train_db():
        tid = tid_entry.get()
        tname = tname_entry.get()
        src = src_entry.get()
        dest = dest_entry.get()
        dep_time = dep_time_entry.get()
        arr_time = arr_time_entry.get()

        if not all([tid, tname, src, dest, dep_time, arr_time]):
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        
        try:
            tid = int(tid)
            datetime.datetime.strptime(dep_time, '%H:%M:%S').time()
            datetime.datetime.strptime(arr_time, '%H:%M:%S').time()
        except ValueError:
            messagebox.showerror("Input Error", "Train ID must be an integer and times must be in HH:MM:SS format.")
            return

        con = connect_db()
        if con:
            try:
                cur = con.cursor()
                
                cur.execute("SELECT train_id FROM trains WHERE train_id = %s", (tid,))
                if cur.fetchone():
                    messagebox.showerror("Input Error", f"Train with ID {tid} already exists.")
                    return

                sql = "INSERT INTO trains (train_id, train_name, source, destination, departure_time, arrival_time) VALUES (%s, %s, %s, %s, %s, %s)"
                cur.execute(sql, (tid, tname, src, dest, dep_time, arr_time))
                
                DEFAULT_CAPACITY = 80
                cur.execute("INSERT INTO bogie_capacity (train_id, seats_per_bogie) VALUES (%s, %s)",
                            (tid, DEFAULT_CAPACITY))

                con.commit()
                messagebox.showinfo("Success", f"Train added successfully!\nTrain ID: {tid}\nBogie Capacity: {DEFAULT_CAPACITY} seats per bogie.")
                go_back(admin_menu)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error adding train: {err}")
                con.rollback()
            finally:
                cur.close()
                con.close()

    ctk.CTkButton(parent_frame, text="Add", command=insert_train_db).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(admin_menu)).pack()

def update_train():
    set_current_frame(lambda parent_frame: _create_update_train_content(parent_frame))

def _create_update_train_content(parent_frame):
    ctk.CTkLabel(parent_frame, text="Update Train", font=("Arial", 24), text_color="white").pack(pady=10)
    
    frame_load = ctk.CTkFrame(parent_frame, fg_color="transparent")
    frame_load.pack(pady=10)
    tid_entry = ctk.CTkEntry(frame_load, placeholder_text="Train ID", width=150)
    tid_entry.pack(side="left", padx=5)
    
    update_fields_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    
    def load_train_details():
        train_id = tid_entry.get()
        if not train_id:
            messagebox.showwarning("Input Error", "Please enter a Train ID.")
            return
        
        con = connect_db()
        if con:
            try:
                cur = con.cursor()
                cur.execute("SELECT train_name, source, destination, departure_time, arrival_time FROM trains WHERE train_id=%s", (train_id,))
                train_data = cur.fetchone()
                
                if train_data:
                    for widget in update_fields_frame.winfo_children():
                        widget.destroy()
                    update_fields_frame.pack(pady=10)
                    
                    new_name_entry = ctk.CTkEntry(update_fields_frame, placeholder_text="New Train Name", width=250)
                    new_name_entry.insert(0, train_data[0])
                    new_name_entry.pack(pady=5)
                    
                    new_src_entry = ctk.CTkEntry(update_fields_frame, placeholder_text="New Source", width=250)
                    new_src_entry.insert(0, train_data[1])
                    new_src_entry.pack(pady=5)
                    
                    new_dest_entry = ctk.CTkEntry(update_fields_frame, placeholder_text="New Destination", width=250)
                    new_dest_entry.insert(0, train_data[2])
                    new_dest_entry.pack(pady=5)
                    
                    ctk.CTkLabel(update_fields_frame, text="New Departure Time (HH:MM:SS):", text_color="white").pack(pady=(10, 0))
                    new_dep_time_entry = ctk.CTkEntry(update_fields_frame, placeholder_text="e.g., 08:30:00", width=250)
                    new_dep_time_entry.insert(0, str(train_data[3]))
                    new_dep_time_entry.pack(pady=5)
                    
                    ctk.CTkLabel(update_fields_frame, text="New Arrival Time (HH:MM:SS):", text_color="white").pack(pady=(10, 0))
                    new_arr_time_entry = ctk.CTkEntry(update_fields_frame, placeholder_text="e.g., 18:00:00", width=250)
                    new_arr_time_entry.insert(0, str(train_data[4]))
                    new_arr_time_entry.pack(pady=5)
                    
                    update_btn = ctk.CTkButton(update_fields_frame, text="Update", command=lambda: do_update(train_id, new_name_entry.get(), new_src_entry.get(), new_dest_entry.get(), new_dep_time_entry.get(), new_arr_time_entry.get()))
                    update_btn.pack(pady=10)
                else:
                    for widget in update_fields_frame.winfo_children():
                        widget.destroy()
                    messagebox.showwarning("Not Found", "No train found with the given ID.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error fetching train details: {err}")
            finally:
                cur.close()
                con.close()

    ctk.CTkButton(frame_load, text="Load Details", command=load_train_details, width=120).pack(side="left", padx=5)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(admin_menu)).pack(pady=10)

def do_update(train_id, new_name, new_src, new_dest, new_dep_time, new_arr_time):
    if not all([train_id, new_name, new_src, new_dest, new_dep_time, new_arr_time]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        datetime.datetime.strptime(new_dep_time, '%H:%M:%S').time()
        datetime.datetime.strptime(new_arr_time, '%H:%M:%S').time()
    except ValueError:
        messagebox.showerror("Input Error", "Times must be in HH:MM:SS format.")
        return

    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            cur.execute("UPDATE trains SET train_name=%s, source=%s, destination=%s, departure_time=%s, arrival_time=%s WHERE train_id=%s",
                        (new_name, new_src, new_dest, new_dep_time, new_arr_time, train_id))
            con.commit()
            if cur.rowcount > 0:
                messagebox.showinfo("Updated", "Train details updated.")
                go_back(admin_menu)
            else:
                messagebox.showwarning("Not Found", "No train found with the given ID.")
                go_back(update_train)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating train: {err}")
            con.rollback()
            go_back(update_train)
        finally:
            cur.close()
            con.close()

def delete_train():
    set_current_frame(lambda parent_frame: _create_delete_train_content(parent_frame))

def _create_delete_train_content(parent_frame):
    ctk.CTkLabel(parent_frame, text="Delete Train", font=("Arial", 24), text_color="white").pack(pady=10)

    tid_entry = ctk.CTkEntry(parent_frame, placeholder_text="Train ID", width=250)
    tid_entry.pack(pady=5)

    def do_delete():
        train_id = tid_entry.get()
        if not train_id:
            messagebox.showwarning("Input Error", "Please enter a Train ID.")
            return

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Train ID {train_id}? This will also delete related reservations."):
            return

        con = connect_db()
        if con:
            try:
                cur = con.cursor()
                cur.execute("DELETE FROM trains WHERE train_id=%s", (train_id,))
                con.commit()
                if cur.rowcount > 0:
                    messagebox.showinfo("Deleted", "Train deleted.")
                else:
                    messagebox.showwarning("Not Found", "No train found with the given ID.")
                go_back(admin_menu)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting train: {err}")
                con.rollback()
            finally:
                cur.close()
                con.close()

    ctk.CTkButton(parent_frame, text="Delete", command=do_delete).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(admin_menu)).pack()

def add_bogie_capacity():
    set_current_frame(lambda parent_frame: _create_add_bogie_capacity_content(parent_frame))

def _create_add_bogie_capacity_content(parent_frame):
    ctk.CTkLabel(parent_frame, text="Add Bogie Capacity", font=("Arial", 24), text_color="white").pack(pady=10)

    train_id_entry = ctk.CTkEntry(parent_frame, placeholder_text="Train ID", width=250)
    train_id_entry.pack(pady=5)

    capacity_entry = ctk.CTkEntry(parent_frame, placeholder_text="Seats per Bogie", width=250)
    capacity_entry.pack(pady=5)

    def do_add_capacity():
        train_id = train_id_entry.get()
        capacity = capacity_entry.get()

        if not all([train_id, capacity]):
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            train_id = int(train_id)
            capacity = int(capacity)
        except ValueError:
            messagebox.showerror("Input Error", "Train ID and Capacity must be numbers.")
            return

        con = connect_db()
        if con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO bogie_capacity (train_id, seats_per_bogie) VALUES (%s, %s) ON DUPLICATE KEY UPDATE seats_per_bogie = %s",
                            (train_id, capacity, capacity))
                con.commit()
                messagebox.showinfo("Success", "Bogie capacity added successfully!")
                go_back(admin_menu)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error adding bogie capacity: {err}")
                con.rollback()
            finally:
                cur.close()
                con.close()

    ctk.CTkButton(parent_frame, text="Add Capacity", command=do_add_capacity).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(admin_menu)).pack()

def view_trains():
    _show_table("SELECT train_id, train_name, source, destination, departure_time, arrival_time FROM trains",
                ["ID", "Name", "From", "To", "Departure", "Arrival"], admin_menu)

def view_passengers():
    _show_table("SELECT passenger_id, name, age, gender, phone_number FROM passenger",
                ["ID", "Name", "Age", "Gender", "Phone"], admin_menu)

def delete_passenger():
    _delete_generic("passenger", "passenger_id", admin_menu)

def view_reservations():
    _show_table("SELECT reservation_id, passenger_id, train_id, travel_date, seat_number, booking_status, bogie_number, coach_type FROM reservations",
                ["ID", "Passenger ID", "Train ID", "Date", "Seat", "Status", "Bogie", "Coach Type"], admin_menu)

def cancel_reservation_admin():
    _delete_generic("reservations", "reservation_id", admin_menu)

def _delete_generic(table_name, id_column, back_func):
    set_current_frame(lambda parent_frame: __create_delete_generic_content(parent_frame, table_name, id_column, back_func))

def __create_delete_generic_content(parent_frame, table_name, id_column, back_func):
    ctk.CTkLabel(parent_frame, text=f"Delete from {table_name}", font=("Arial", 24), text_color="white").pack(pady=10)

    entry_id = ctk.CTkEntry(parent_frame, placeholder_text=f"{id_column.replace('_', ' ').title()}", width=250)
    entry_id.pack(pady=5)

    def do_delete():
        item_id = entry_id.get()
        if not item_id:
            messagebox.showwarning("Input Error", f"Please enter the {id_column.replace('_', ' ').title()}.")
            return
        
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {table_name[:-1]} with ID {item_id}?"):
            return

        con = connect_db()
        if con:
            try:
                cur = con.cursor()
                cur.execute(f"DELETE FROM {table_name} WHERE {id_column}=%s", (item_id,))
                con.commit()
                if cur.rowcount > 0:
                    messagebox.showinfo("Deleted", f"Deleted from {table_name}.")
                else:
                    messagebox.showwarning("Not Found", f"No {table_name[:-1]} found with the given ID.")
                go_back(back_func)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting from {table_name}: {err}")
                con.rollback()
            finally:
                cur.close()
                con.close()

    ctk.CTkButton(parent_frame, text="Delete", command=do_delete).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(back_func)).pack()

def user_menu():
    set_current_frame(lambda parent_frame: _create_user_menu_content(parent_frame))

def _create_user_menu_content(parent_frame):
    ctk.CTkLabel(parent_frame, text="Welcome, Passenger", font=("Arial", 26), text_color="white").pack(pady=30)

    ctk.CTkButton(parent_frame, text="Book Ticket", command=book_ticket, width=250, height=50).pack(pady=10)
    ctk.CTkButton(parent_frame, text="View My Reservation", command=view_user_reservation, width=250, height=50).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Cancel My Ticket", command=cancel_user_reservation, width=250, height=50).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(main_menu), width=250, height=50).pack(pady=10)

def cancel_user_reservation():
    set_current_frame(lambda parent_frame: _create_cancel_user_reservation_content(parent_frame))

def _create_cancel_user_reservation_content(parent_frame):
    ctk.CTkLabel(parent_frame, text="Cancel Your Ticket", font=("Arial", 24), text_color="white").pack(pady=10)

    reservation_id_entry = ctk.CTkEntry(parent_frame, placeholder_text="Enter Reservation ID", width=250)
    reservation_id_entry.pack(pady=5)

    def confirm_cancellation():
        reservation_id = reservation_id_entry.get()

        if not reservation_id:
            messagebox.showwarning("Input Error", "Please enter a Reservation ID.")
            return

        if not messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel reservation with ID {reservation_id}?"):
            return

        con = connect_db()
        if con:
            try:
                cur = con.cursor()
                
                cur.execute("SELECT passenger_id FROM reservations WHERE reservation_id = %s", (reservation_id,))
                passenger_id_to_delete = cur.fetchone()
                
                if not passenger_id_to_delete:
                    messagebox.showwarning("Not Found", f"No reservation found with ID {reservation_id}.")
                    con.close()
                    return
                
                passenger_id = passenger_id_to_delete[0]

                cur.execute("DELETE FROM reservations WHERE reservation_id=%s", (reservation_id,))
                
                cur.execute("SELECT COUNT(*) FROM reservations WHERE passenger_id=%s", (passenger_id,))
                other_reservations = cur.fetchone()[0]

                if other_reservations == 0:
                    cur.execute("DELETE FROM passenger WHERE passenger_id=%s", (passenger_id,))
                    con.commit()
                    messagebox.showinfo("Cancellation Successful", f"Reservation with ID {reservation_id} and the corresponding passenger record have been canceled.")
                else:
                    con.commit()
                    messagebox.showinfo("Cancellation Successful", f"Reservation with ID {reservation_id} has been canceled.")
                
                go_back(user_menu)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error canceling reservation: {err}")
                con.rollback()
            finally:
                if con and con.is_connected():
                    cur.close()
                    con.close()

    ctk.CTkButton(parent_frame, text="Cancel Reservation", command=confirm_cancellation).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(user_menu)).pack()

def book_ticket():
    set_current_frame(lambda parent_frame: _create_book_ticket_content(parent_frame))

def allocate_seat_backend(train_id, travel_date, coach_type):
    con = connect_db()
    if not con:
        return None, None, "Error"
    
    COACH_CAPACITIES = {
        "Sleeper": 72,
        "3rd AC": 64,
        "2nd AC": 46,
        "1st AC": 24
    }
    
    seats_per_bogie = COACH_CAPACITIES.get(coach_type, 72)
    total_capacity = 20 * seats_per_bogie
    
    try:
        cur = con.cursor()
        
        cur.execute("SELECT COUNT(*) FROM reservations WHERE train_id=%s AND travel_date=%s AND coach_type=%s AND booking_status='Confirmed'",
                    (train_id, travel_date, coach_type))
        confirmed_bookings = cur.fetchone()[0]
        
        if confirmed_bookings >= total_capacity:
            return None, None, 'Waiting'
        else:
            seat_index = confirmed_bookings + 1
            bogie_number = chr(ord('A') + (seat_index - 1) // seats_per_bogie)
            seat_number = (seat_index - 1) % seats_per_bogie + 1
            
            return bogie_number, str(seat_number), 'Confirmed'
    
    except mysql.connector.Error as err:
        print(f"Database Error in seat allocation: {err}")
        return None, None, "Error"
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

def _create_book_ticket_content(parent_frame):
    con = connect_db()
    train_options_data = []
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT train_id, train_name, source, destination, departure_time, arrival_time FROM trains")
            train_options_data = cur.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching trains: {err}")
        finally:
            cur.close()
            con.close()

    train_map = {f"{t[1]} ({t[2]} ➜ {t[3]})": {'id': t[0], 'departure': t[4], 'arrival': t[5]} for t in train_options_data}
    train_display_options = [f"{t[1]} ({t[2]} ➜ {t[3]}) - Dep: {t[4]} / Arr: {t[5]}" for t in train_options_data]
    
    if not train_display_options:
        train_display_options = ["No Trains Available"]

    ctk.CTkLabel(parent_frame, text="Book Ticket", font=("Arial", 24), text_color="white").pack(pady=10)

    name_entry = ctk.CTkEntry(parent_frame, placeholder_text="Name", width=250)
    name_entry.pack(pady=5)

    age_entry = ctk.CTkEntry(parent_frame, placeholder_text="Age", width=250)
    age_entry.pack(pady=5)

    gender_entry = ctk.CTkEntry(parent_frame, placeholder_text="Gender", width=250)
    gender_entry.pack(pady=5)

    phone_entry = ctk.CTkEntry(parent_frame, placeholder_text="Phone Number", width=250)
    phone_entry.pack(pady=5)

    train_dropdown = ctk.CTkOptionMenu(parent_frame, values=train_display_options)
    train_dropdown.set(train_display_options[0])
    train_dropdown.pack(pady=5)
    
    coach_type_options = ["Sleeper", "3rd AC", "2nd AC", "1st AC"]
    coach_type_dropdown = ctk.CTkOptionMenu(parent_frame, values=coach_type_options)
    coach_type_dropdown.set("Sleeper")
    coach_type_dropdown.pack(pady=5)

    ctk.CTkLabel(parent_frame, text="Select Travel Date:", text_color="white").pack(pady=(10, 5))
    calendar_frame = ctk.CTkFrame(parent_frame, fg_color="black")
    calendar_frame.pack(pady=5)
    calendar = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd', background="#343638", bordercolor="#343638",
                        headersbackground="#343638", normalbackground="#343638", foreground="white", headersforeground="white",
                        normalforeground="white", selectbackground="#1f538d", selectforeground="white")
    calendar.pack()
    
    def confirm_booking():
        p_name = name_entry.get()
        p_age = age_entry.get()
        p_gender = gender_entry.get()
        p_phone = phone_entry.get()
        selected_train_display = train_dropdown.get()
        selected_coach_type = coach_type_dropdown.get()
        
        travel_date_str = calendar.get_date()
        
        if not all([p_name, p_age, p_gender, p_phone, selected_train_display, selected_coach_type, travel_date_str]):
            messagebox.showwarning("Input Error", "All fields are required for booking!")
            return

        try:
            p_age = int(p_age)
            if p_age <= 0:
                raise ValueError("Age must be a positive number.")
            travel_date = datetime.date.fromisoformat(travel_date_str)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}\nAge must be a number.")
            return
        
        selected_train_info = None
        for display_string, info in train_map.items():
            if selected_train_display.startswith(display_string):
                selected_train_info = info
                break
        
        if not selected_train_info:
            messagebox.showerror("Booking Error", "Selected train information not found.")
            return
        
        train_id = selected_train_info['id']

        bogie_number, seat_num, booking_status = allocate_seat_backend(train_id, travel_date_str, selected_coach_type)
        
        if booking_status == 'Error':
            messagebox.showerror("Booking Error", "An error occurred during seat allocation. Please try again.")
            return
        
        if booking_status == 'No Capacity Defined':
            messagebox.showerror("Booking Error", f"Capacity not defined for this train. Booking cannot be made.")
            return

        con = connect_db()
        if con:
            try:
                cur = con.cursor()
                
                cur.execute("SELECT passenger_id FROM passenger ORDER BY passenger_id DESC LIMIT 1")
                last_p_id = cur.fetchone()
                if last_p_id:
                    passenger_id = last_p_id[0] + 1
                else:
                    passenger_id = 1
                
                cur.execute("INSERT INTO passenger (passenger_id, name, age, gender, phone_number) VALUES (%s, %s, %s, %s, %s)",
                            (passenger_id, p_name, p_age, p_gender, p_phone))
                
                cur.execute("SELECT reservation_id FROM reservations ORDER BY reservation_id DESC LIMIT 1")
                last_res_id = cur.fetchone()
                if last_res_id:
                    reservation_id = last_res_id[0] + 1
                else:
                    reservation_id = 1
                
                global current_passenger_id
                current_passenger_id = passenger_id
                
                cur.execute("INSERT INTO reservations (reservation_id, passenger_id, train_id, travel_date, seat_number, booking_status, bogie_number, coach_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (reservation_id, passenger_id, train_id, travel_date, seat_num, booking_status, bogie_number, selected_coach_type))
                con.commit()
                
                if booking_status == 'Confirmed':
                    messagebox.showinfo("Success", f"Ticket booked!\nYour Passenger ID: {passenger_id}\nReservation ID: {reservation_id}\nBogie: {bogie_number}\nSeat Number: {seat_num}\nCoach Type: {selected_coach_type}")
                else:
                    messagebox.showinfo("Waitlist", f"Train is full. You have been added to the waiting list with Reservation ID: {reservation_id}.")

                go_back(user_menu)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error making reservation: {err}")
                con.rollback()
            finally:
                cur.close()
                con.close()

    ctk.CTkButton(parent_frame, text="Confirm Booking", command=confirm_booking, width=150, height=30).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(user_menu), width=150, height=30).pack(pady=5)

def view_user_reservation():
    set_current_frame(lambda parent_frame: _create_view_user_reservation_content(parent_frame))

def _create_view_user_reservation_content(parent_frame):
    ctk.CTkLabel(parent_frame, text="View Your Reservation", font=("Arial", 24), text_color="white").pack(pady=10)
    
    pid_entry = ctk.CTkEntry(parent_frame, placeholder_text="Enter Your Passenger ID", width=250)
    pid_entry.pack(pady=5)

    if current_passenger_id:
        pid_entry.insert(0, str(current_passenger_id))

    table_display_area = ctk.CTkFrame(parent_frame, fg_color="black")
    table_display_area.pack(pady=10, padx=10, fill="both", expand=True)
    
    table_display_area.grid_rowconfigure(0, weight=1)
    table_display_area.grid_columnconfigure(0, weight=1)

    def fetch_user_reservations():
        for widget in table_display_area.winfo_children():
            widget.destroy()

        passenger_id = pid_entry.get()
        if not passenger_id:
            messagebox.showwarning("Input Error", "Please enter your Passenger ID.")
            return
        
        try:
            passenger_id = int(passenger_id)
        except ValueError:
            messagebox.showerror("Input Error", "Passenger ID must be a number.")
            return

        con = connect_db()
        rows = []
        if con:
            try:
                cur = con.cursor()
                query = """
                    SELECT
                        r.reservation_id,
                        r.passenger_id,
                        t.train_name,
                        t.source,
                        t.destination,
                        r.coach_type,
                        t.departure_time,
                        t.arrival_time,
                        r.travel_date,
                        r.seat_number,
                        r.booking_status,
                        r.bogie_number
                    FROM
                        reservations r
                    JOIN
                        trains t ON r.train_id = t.train_id
                    WHERE
                        r.passenger_id = %s
                """
                cur.execute(query, (passenger_id,))
                rows = cur.fetchall()

                if not rows:
                    messagebox.showinfo("No Reservations", f"No reservations found for Passenger ID {passenger_id}.")
                
                cols = ["Reservation ID", "Passenger ID", "Train Name", "Source", "Destination",
                        "Coach Type", "Departure Time", "Arrival Time", "Travel Date", "Seat Number", "Status", "Bogie"]
                
                _show_table_data(rows, cols, user_menu, parent_frame=table_display_area)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error fetching reservations: {err}")
            finally:
                if con:
                    cur.close()
                    con.close()

    ctk.CTkButton(parent_frame, text="View", command=fetch_user_reservations).pack(pady=10)
    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(user_menu)).pack(pady=10)

def _show_table(query, cols, back_func):
    set_current_frame(lambda parent_frame: __create_show_table_content(parent_frame, query, cols, back_func))

def __create_show_table_content(parent_frame, query, cols, back_func):
    table_container_frame = ctk.CTkFrame(parent_frame, fg_color="black")
    table_container_frame.pack(expand=True, fill="both", pady=10, padx=10)
    
    table_container_frame.grid_rowconfigure(0, weight=1)
    table_container_frame.grid_columnconfigure(0, weight=1)

    con = connect_db()
    rows = []
    if con:
        try:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")
        finally:
            if con:
                cur.close()
                con.close()

    _show_table_data(rows, cols, back_func, parent_frame=table_container_frame)

    ctk.CTkButton(parent_frame, text="Go Back", command=lambda: go_back(back_func)).pack(pady=20)


def _show_table_data(rows, cols, back_func, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    table = ttk.Treeview(parent_frame, columns=cols, show="headings")
    
    style = ttk.Style(parent_frame)
    style.theme_use("clam")
    style.configure("Treeview", 
                    background="#2b2b2b", 
                    foreground="white",
                    fieldbackground="#2b2b2b",
                    borderwidth=0)
    style.map('Treeview', 
              background=[('selected', '#1f538d')])
    
    style.configure("Treeview.Heading",
                    background="#1f538d",
                    foreground="white",
                    font=('Arial', 10, 'bold'))

    vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=table.yview)
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    table.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)
    vsb.grid(row=0, column=1, sticky="ns", pady=10)
    hsb.grid(row=1, column=0, sticky="ew", padx=10)
    
    parent_frame.grid_rowconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(1, weight=0)

    for col in cols:
        table.heading(col, text=col)
        col_width = 100
        if "ID" in col or "Age" in col or "Seat" in col:
            col_width = 70
        elif "Name" in col or "Source" in col or "Destination" in col:
            col_width = 150
        elif "Date" in col or "Status" in col or "Bogie" in col or "Coach" in col:
            col_width = 120
        elif "Phone" in col:
            col_width = 110
        elif "Time" in col:
            col_width = 100

        table.column(col, width=col_width, anchor="center")
        if "Name" in col or "Source" in col or "Destination" in col or "Coach" in col:
            table.column(col, anchor="w")

    for row in rows:
        formatted_row = []
        for item in row:
            if isinstance(item, datetime.date):
                formatted_row.append(item.strftime("%Y-%m-%d"))
            elif isinstance(item, datetime.time):
                formatted_row.append(item.strftime("%H:%M:%S"))
            else:
                formatted_row.append(str(item))

        if len(formatted_row) < len(cols):
            padded_row = formatted_row + ['N/A'] * (len(cols) - len(formatted_row))
            table.insert("", "end", values=tuple(padded_row))
        elif len(formatted_row) > len(cols):
            truncated_row = formatted_row[:len(cols)]
            table.insert("", "end", values=tuple(truncated_row))
        else:
            table.insert("", "end", values=tuple(formatted_row))

if __name__ == "__main__":
    main_menu()
    app.mainloop()
