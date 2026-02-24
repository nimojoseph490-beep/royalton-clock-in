import tkinter as tk
from tkinter import messagebox
import subprocess # This allows the button to "trigger" your scanner script

def start_scanning():
    try:
        # This tells Python to run your scanner script when the button is clicked
        subprocess.Popen(['python3', 'Scanner.py'])
        status_label.config(text="Status: Scanner Active ✅", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Could not start scanner: {e}")

# 1. Create the Main Window
root = tk.Tk()
root.title("Royalton International School - Clock-In System")
root.geometry("500x400")
root.configure(bg="#f0f0f0") # Light grey background

# 2. Add a Header
header = tk.Label(root, text="ROYALTON INTERNATIONAL", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#1a237e")
header.pack(pady=20)

# 3. Add an Instruction Label
instruction = tk.Label(root, text="Please have your QR Code ready", font=("Arial", 12), bg="#f0f0f0")
instruction.pack(pady=10)

# 4. The "Start" Button
scan_button = tk.Button(root, text="START SCANNER", command=start_scanning, 
                        font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                        padx=20, pady=10, cursor="hand2")
scan_button.pack(pady=30)

# 5. Status Footer
status_label = tk.Label(root, text="Status: Ready", font=("Arial", 10, "italic"), bg="#f0f0f0")
status_label.pack(side="bottom", pady=20)

# Run the Interface
root.mainloop()