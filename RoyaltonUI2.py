import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from pyzbar.pyzbar import decode
import datetime
import sqlite3

def scan_from_file():
    # 1. Open a window to pick the image file
    file_path = filedialog.askopenfilename(
        title="Select Student QR Code",
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    
    if not file_path:
        return

    # 2. Read the image using OpenCV
    img = cv2.imread(file_path)
    
    # 3. Decode the QR code
    detected_codes = decode(img)
    
    if not detected_codes:
        messagebox.showerror("Error", "No QR code found in that image. Try a clearer photo!")
        return

    for code in detected_codes:
        student_data = code.data.decode('utf-8')
        arrival_time = datetime.datetime.now().strftime("%I:%M %p")
        
        # Show success message
        messagebox.showinfo("Success", f"Student Identified: {student_data}\nLogged at: {arrival_time}")
        
        # Update UI label
        status_label.config(text=f"Last Scan: {student_data}", fg="green")

# --- UI Setup ---
root = tk.Tk()
root.title("Royalton International School - Digital Office")
root.geometry("500x450")
root.configure(bg="#f0f0f0")

header = tk.Label(root, text="ROYALTON INTERNATIONAL", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#1a237e")
header.pack(pady=20)

# The New Button
upload_button = tk.Button(root, text="UPLOAD QR PHOTO", command=scan_from_file, 
                          font=("Arial", 14, "bold"), bg="#2196F3", fg="white", 
                          padx=20, pady=10, cursor="hand2")
upload_button.pack(pady=30)

status_label = tk.Label(root, text="Status: Ready to Upload", font=("Arial", 10, "italic"), bg="#f0f0f0")
status_label.pack(side="bottom", pady=20)

root.mainloop()