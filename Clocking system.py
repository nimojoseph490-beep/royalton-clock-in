#import current date and time
import datetime
current_time = datetime.datetime.now()
readable_time = current_time.strftime("%H:%M:%S")
print("Welcome to Royalton International School!")
print(f"System started at: {readable_time}")
#Ask for student details 
student_name = input("Name of student")
student_id = input("Student ID")
print("CLOCK IN SUCCESSFUL!")
print(f"Student: {student_name}")
print(f"ID: {student_id}")
print(f"Clocked in at {readable_time}")