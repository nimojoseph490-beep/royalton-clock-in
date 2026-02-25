import os
import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# MANDATORY FOR RENDER SQLITE: Use /tmp folder
DB_PATH = '/tmp/attendance.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS attendance (student_id TEXT, date TEXT, time TEXT)")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Startup Database Error: {e}")

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
    try:
        display_name = request.json.get('name')
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.datetime.now().strftime("%I:%M %p")
        
        # Generate ID just like your original Tkinter version
        student_id = f"RIS-{display_name[:3].upper()}001"
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)", 
                    (display_name, today, now_time))
        conn.commit()
        cur.close()
        conn.close()

        # Build the full detailed success message for the popup
        full_message = (
            f"Student: {display_name}\n"
            f"ID: {student_id}\n"
            f"Time: {now_time}\n\n"
            "Enjoy your day at school! 🎓"
        )
        
        # We send 'last_scan' back so the website can update the label
        return jsonify({
            "status": "success", 
            "message": full_message, 
            "last_scan": display_name
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/history')
def history():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT student_id, date, time FROM attendance ORDER BY date DESC, time DESC LIMIT 100")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        table_html = """
        <html>
        <head><style>
            table { width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #f2f2f2; }
        </style></head>
        <body>
            <h1>Attendance History (Last 100)</h1>
            <table><tr><th>Student Name</th><th>Date</th><th>Time</th></tr>
        """
        for r in rows:
            table_html += f"<tr><td>{r['student_id']}</td><td>{r['date']}</td><td>{r['time']}</td></tr>"
        
        return table_html + "</table><br><a href='/'>Back to Scanner</a></body></html>"
    except Exception as e:
        return f"Error loading history: {e}"

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)