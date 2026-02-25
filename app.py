import os
import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Helper to connect to your existing database
def get_db_connection():
    conn = sqlite3.connect('royalton_school.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ensure the table exists
def init_db():
    conn = get_db_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS attendance (student_id TEXT, date TEXT, time TEXT)")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# Mimics your Tkinter update_suggestions
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    suggestions = []
    if os.path.exists('student_qrs'):
        for file in os.listdir('student_qrs'):
            if query in file.lower():
                display_name = file.replace('_', ' ').replace('.png', '')
                suggestions.append(display_name)
    return jsonify(suggestions)

# Mimics your Tkinter process_qr_scan / save_to_db
@app.route('/log_attendance', methods=['POST'])
def log_attendance():
    display_name = request.json.get('name')
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.datetime.now().strftime("%I:%M %p")
    
    # Generate ID just like your Tkinter code
    student_id = f"RIS-{display_name[:3].upper()}001"
    
    conn = get_db_connection()
    conn.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)", 
                (display_name, today, now_time))
    conn.commit()
    conn.close()

    # The exact message from your Tkinter app
    display_message = (
        f"Student: {display_name}\n"
        f"ID: {student_id}\n"
        f"Time: {now_time}\n\n"
        "Enjoy your day at school! 🎓"
    )
    
    return jsonify({"status": "success", "message": display_message, "last_scan": display_name})

# Mimics your Tkinter show_attendance / load_data
@app.route('/get_logs')
def get_logs():
    selected_date = request.args.get('date') # Format from web: YYYY-MM-DD
    conn = get_db_connection()
    rows = conn.execute("SELECT student_id, time FROM attendance WHERE date = ?", (selected_date,)).fetchall()
    conn.close()
    
    # Convert database rows into a list the website can read
    return jsonify([{"id": r["student_id"], "time": r["time"]} for r in rows])


if __name__ == "__main__":
    # Get the port from Render's environment, or use 10000 as default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)