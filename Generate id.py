import qrcode
#student details
name = "Nimo Joseph"
id_num = "RIS-2024-001"
data = f"ID:{id_num}, Name:{name}"
print(f"Genarating QR Code for {name}...")
#Create the QR Code
image = qrcode.make(data)
#Save it
image.save("Student_qr.png")
print("Success! Check your file list for 'Student_qr.png'")