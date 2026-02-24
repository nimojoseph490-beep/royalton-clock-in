import cv2
from pyzbar.pyzbar import decode
import datetime
import sqlite3

# Start camera
cap = cv2.VideoCapture(0)

print("Scanner Active... waiting for camera...")

while True:
    success, frame = cap.read()
    
    # SAFETY CHECK: If camera isn't ready yet, wait a millisecond and try again
    if not success or frame is None:
        cv2.waitKey(1)
        continue

    # Search for QR codes
    for code in decode(frame):
        student_data = code.data.decode('utf-8')
        arrival_time = datetime.datetime.now().strftime("%I:%M %p")
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        print(f"✅ Success: {student_data} at {arrival_time}")

        # OPTIONAL: Save to Database
        try:
            conn = sqlite3.connect('royalton_school.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)", 
                           (student_data, today_date, arrival_time))
            conn.commit()
            conn.close()
        except:
            print("Note: Database not found, just printing to screen.")

        cap.release()
        cv2.destroyAllWindows()
        exit()

    cv2.imshow('Royalton Scanner Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()