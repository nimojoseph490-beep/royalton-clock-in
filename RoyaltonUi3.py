import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk  # Added ttk here
import cv2
from pyzbar.pyzbar import decode
import datetime
import sqlite3

# --- 1. THE DATABASE SAVE LOGIC ---
def save_to_db(student_info):
    try:
        conn = sqlite3.connect('royalton_school.db')
        cursor = conn.cursor()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.datetime.now().strftime("%I:%M %p")
        
        cursor.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)", 
                       (student_info, today, now_time))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database save failed: {e}")

# --- 2. THE SCANNING LOGIC ---
def process_qr_scan(file_path):
    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Could not read the QR image file.")
        return
        
    detected = decode(img)
    if detected:
        for code in detected:
            data = code.data.decode('utf-8')
            # Split data if it has a "|" separator from our generator
            display_name = data.split('|')[0].strip() if '|' in data else data
            student_id = data.split('|')[1].strip() if '|' in data else f"RIS-{data[:3].upper()}001"
            
            arrival_time = datetime.datetime.now().strftime("%I:%M %p")
            
            # The complete message you requested
            display_message = (
                f"Student: {display_name}\n"
                f"ID: {student_id}\n"
                f"Time: {arrival_time}\n\n"
                "Enjoy your day at school! 🎓"
            )
            
            save_to_db(display_name) 
            messagebox.showinfo("Entry Logged", display_message)
            status_label.config(text=f"Last Scan: {display_name}", fg="green")
    else:
        messagebox.showerror("Error", "QR code could not be decoded.")

# --- 3. THE VIEW LOG LOGIC ---
def show_attendance():
    # 1. Create a small window to ask for the date
    date_win = tk.Toplevel(root)
    date_win.title("Select Date")
    date_win.geometry("300x150")
    
    tk.Label(date_win, text="Enter Date (YYYY-MM-DD):").pack(pady=10)
    
    # Pre-fill with today's date so it's easier for the user
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    date_entry = tk.Entry(date_win)
    date_entry.insert(0, today_str)
    date_entry.pack(pady=5)

    def load_data():
        selected_date = date_entry.get()
        date_win.destroy() # Close the small box
        
        # 2. Create the main Log Window
        log_win = tk.Toplevel(root)
        log_win.title(f"Attendance Log for {selected_date}")
        log_win.geometry("600x400")

        columns = ('ID', 'Status', 'Time')
        tree = ttk.Treeview(log_win, columns=columns, show='headings')
        tree.heading('ID', text='Student Name/ID')
        tree.heading('Status', text='Status')
        tree.heading('Time', text='Time In')
        tree.pack(fill='both', expand=True)

        # 3. Fetch from Database based on the date entered
        try:
            conn = sqlite3.connect('royalton_school.db')
            cur = conn.cursor()
            cur.execute("SELECT student_id, 'Present', time FROM attendance WHERE date = ?", (selected_date,))
            rows = cur.fetchall()
            
            if not rows:
                messagebox.showinfo("No Data", f"No one scanned in on {selected_date}")
                log_win.destroy()
            else:
                for row in rows:
                    tree.insert('', tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Button to confirm the date
    tk.Button(date_win, text="Show Logs", command=load_data, bg="#4CAF50", fg="white").pack(pady=10)   
def update_suggestions(event):
    search_term = search_entry.get().lower()
    suggestion_list.delete(0, tk.END)
    
    if search_term:
        # Show the list only when typing
        suggestion_list.pack(pady=5, padx=20, fill='x')
        for file in os.listdir('student_qrs'):
            if search_term in file.lower():
                display_name = file.replace('_', ' ').replace('.png', '')
                suggestion_list.insert(tk.END, display_name)
    else:
        # Hide the list if the search bar is empty
        suggestion_list.pack_forget()

def select_student(event):
    if not suggestion_list.curselection():
        return
    selection = suggestion_list.get(suggestion_list.curselection())
    search_entry.delete(0, tk.END)
    search_entry.insert(0, selection)
    suggestion_list.pack_forget() # Hide list after selection
    
    # Trigger the scan automatically
    file_to_scan = f"student_qrs/{selection.replace(' ', '_')}.png"
    process_qr_scan(file_to_scan)
# --- 4. THE INTERFACE SETUP ---
# --- Interface Setup ---
root = tk.Tk()
root.title("Royalton International School")
root.geometry("500x650")
root.configure(bg="#f0f0f0")

# 1. The Logo (From your uploaded screenshot)
try:
    logo_img = tk.PhotoImage(file="logo.png").subsample(2, 2)
    tk.Label(root, image=logo_img, bg="#f0f0f0").pack(pady=10)
except:
    tk.Label(root, text="ROYALTON INTERNATIONAL", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=10)

# 2. The Search Area
tk.Label(root, text="TYPE STUDENT NAME:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)
search_entry = tk.Entry(root, font=("Arial", 14), bd=2, relief="groove")
search_entry.pack(pady=5, padx=30, fill='x')
search_entry.bind('<KeyRelease>', update_suggestions)

# 3. The Suggestions List (This will appear/disappear)
suggestion_list = tk.Listbox(root, height=6, font=("Arial", 12))
suggestion_list.bind('<<ListboxSelect>>', select_student)

# 4. History Button
tk.Button(root, text="VIEW HISTORY LOG", command=show_attendance, bg="#607D8B", fg="white").pack(pady=20)

status_label = tk.Label(root, text="System Ready", font=("Arial", 10, "italic"), bg="#f0f0f0")
status_label.pack(side="bottom", pady=10)

root.mainloop()