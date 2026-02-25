import os
import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Helper to connect to SQLite
def get_db_connection():
    # This creates/opens attendance.db in your project folder
    conn = sqlite3.connect('attendance.db')
    return conn

# Ensure the table exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS attendance (student_id TEXT, date TEXT, time TEXT)")
    conn.commit()
    cur.close()
    conn.close()

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/log_attendance', methods=['POST'])
def log_attendance():
    display_name = request.json.get('name')
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.datetime.now().strftime("%I:%M %p")
    student_id = f"RIS-{display_name[:3].upper()}001"
    
    conn = get_db_connection()
    cur = conn.cursor()
    # Note: SQLite uses '?' as a placeholder
    cur.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)", 
                (display_name, today, now_time))
    conn.commit()
    cur.close()
    conn.close()

    display_message = (
        f"Student: {display_name}\n"
        f"ID: {student_id}\n"
        f"Time: {now_time}\n\n"
        "Enjoy your day at school! 🎓"
    )
    return jsonify({"status": "success", "message": display_message, "last_scan": display_name})

@app.route('/get_logs')
def get_logs():
    selected_date = request.args.get('date')
    conn = get_db_connection()
    cur = conn.cursor()
    # Note: SQLite uses '?' as a placeholder
    cur.execute("SELECT student_id, time FROM attendance WHERE date = ?", (selected_date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "time": r[1]} for r in rows])

# NEW: The History Page to view logs on the site
@app.route('/history')
def history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id, date, time FROM attendance ORDER BY date DESC, time DESC LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    table_html = """
    <html>
    <head><title>Attendance Logs</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>Attendance History (Last 100 Scans)</h1>
        <table border="1" style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #f2f2f2;">
                <th>Student Name</th><th>Date</th><th>Time</th>
            </tr>
    """
    for r in rows:
        table_html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    
    table_html += "</table><br><a href='/'>Back to Scanner</a></body></html>"
    return table_html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)