import qrcode
import os

# 1. The Student List (Add your students here)
# Format: "Name": "ID"
students = {
    "Appiah Promise": "RIS-G1-001",
    "Asante Emmanuel": "RIS-G2-001",
    "Nsiah Sophia": "RIS-G3-001"
}

# 2. Create a folder to store the images
if not os.path.exists('student_qrs'):
    os.makedirs('student_qrs')

# 3. The Loop to create each QR
for name, student_id in students.items():
    # Combine name and ID into the QR data
    qr_data = f"{name} | {student_id}"
    
    # Generate the QR
    qr = qrcode.make(qr_data)
    
    # Save the file as 'StudentName.png'
    file_name = f"student_qrs/{name.replace(' ', '_')}.png"
    qr.save(file_name)
    
    print(f"Generated: {file_name}")

print("\nAll student QR codes are ready in the 'student_qrs' folder!")