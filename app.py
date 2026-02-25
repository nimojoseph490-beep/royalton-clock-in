import os
import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# MANDATORY FOR RENDER SQLITE: Use /tmp folder
# Render will crash if you try to write to the root folder.
DB_PATH = '/tmp/attendance.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# We wrap this in a try/except so if the DB fails, the PORT still opens
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS attendance (student_id TEXT, date TEXT, time TEXT)")
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully connected to database at {DB_PATH}")
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
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)", 
                    (display_name, today, now_time))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "message": f"Logged {display_name}"})
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

        table_html = "<h1>Attendance History</h1><table border='1'><tr><th>ID</th><th>Date</th><th>Time</th></tr>"
        for r in rows:
            table_html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        return table_html + "</table><br><a href='/'>Back</a>"
    except Exception as e:
        return f"Error: {e}"

# Move init_db down here so the app is ready to start immediately
init_db()

if __name__ == "__main__":
    # If this part doesn't run, Render gives the "No open ports" error
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting app on port {port}...")
    app.run(host='0.0.0.0', port=port)