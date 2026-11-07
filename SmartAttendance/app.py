import os
import secrets
import sqlite3
import time
from functools import wraps

from flask import Flask, Response, jsonify, redirect, render_template, request, session


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

# Development password only. Replace with real backend authentication before deployment.
TEACHER_PASSWORD = "12345"


def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            class_id INTEGER,
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS student_courses (
            student_id TEXT NOT NULL,
            class_id INTEGER NOT NULL,
            PRIMARY KEY (student_id, class_id),
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')
    db.execute("INSERT OR IGNORE INTO classes (id, name) VALUES (1, 'Physics 101')")
    db.execute("INSERT OR IGNORE INTO classes (id, name) VALUES (2, 'Computer Science 204')")
    db.execute('''
        INSERT OR IGNORE INTO student_courses (student_id, class_id)
        SELECT id, class_id FROM students WHERE class_id IS NOT NULL
    ''')
    db.commit()
    db.close()

init_db()

current_session = {
    'code': None,
    'class_id': None,
    'expires_at': None,
    'present_students': []
}


def teacher_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("teacher_authenticated"):
            return redirect("/teacher/login")
        return view(*args, **kwargs)
    return wrapped


@app.route("/", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        session_code = request.form.get("session_code", "").strip()
        class_id = request.form.get("class_id", "").strip()
        if not student_id or not session_code or not class_id:
            return "Student ID, class, and session code are required.", 400
        try:
            if class_id and int(class_id) != current_session["class_id"]:
                return "The scanned class does not match the active attendance session.", 403
        except ValueError:
            return "Invalid class number.", 400
        if (
            not current_session["code"]
            or current_session["expires_at"] is None
            or current_session["code"] != session_code
            or time.time() >= current_session["expires_at"]
        ):
            return "Invalid session code or session expired.", 403

        db = get_db()
        student = db.execute(
            '''SELECT students.id FROM students
               JOIN student_courses ON student_courses.student_id = students.id
               WHERE students.id = ? AND student_courses.class_id = ?''',
            (student_id, current_session["class_id"]),
        ).fetchone()
        db.close()
        if not student:
            return "Student ID not found in this class.", 404
        if student_id in current_session["present_students"]:
            return "You have already been marked as present."
        current_session["present_students"].append(student_id)
        return "Successfully checked in!"
    db = get_db()
    classes = db.execute("SELECT id, name FROM classes ORDER BY name").fetchall()
    db.close()
    return render_template("student_login.html", classes=classes)


@app.route("/teacher/login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if TEACHER_PASSWORD and secrets.compare_digest(password, TEACHER_PASSWORD):
            session["teacher_authenticated"] = True
            return redirect("/teacher")
        return render_template("teacher_login.html", error=True), 401
    return render_template("teacher_login.html", error=False)


@app.route("/teacher/logout", methods=["POST"])
def teacher_logout():
    session.pop("teacher_authenticated", None)
    return redirect("/teacher/login")


@app.route("/teacher")
@teacher_required
def teacher_dashboard():
    db = get_db()
    classes = db.execute('SELECT * FROM classes ORDER BY name').fetchall()
    student_rows = db.execute('SELECT id, name FROM students ORDER BY name, id').fetchall()
    students = []
    for student in student_rows:
        course_rows = db.execute(
            '''SELECT classes.id, classes.name FROM classes
               JOIN student_courses ON student_courses.class_id = classes.id
               WHERE student_courses.student_id = ? ORDER BY classes.name''',
            (student["id"],),
        ).fetchall()
        students.append({
            "id": student["id"],
            "name": student["name"],
            "courses": course_rows,
        })
    db.close()
    return render_template("teacher_dashboard.html", classes=classes, students=students)


@app.route("/api/classes", methods=["POST"])
@teacher_required
def add_class():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"error": "Class name is required"}), 400
    db = get_db()
    db.execute("INSERT INTO classes (name) VALUES (?)", (name,))
    db.commit()
    class_id = db.execute("SELECT id FROM classes WHERE name = ?", (name,)).fetchone()["id"]
    db.close()
    return jsonify({"id": class_id, "name": name}), 201


@app.route("/api/students", methods=["POST"])
@teacher_required
def add_student():
    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    name = str(data.get("name", "")).strip()
    class_id = data.get("class_id")
    class_ids = data.get("class_ids")
    if class_ids is None:
        class_ids = [class_id] if class_id else []
    class_ids = list(dict.fromkeys(str(value) for value in class_ids if value is not None))
    if not student_id or not name or not class_ids:
        return jsonify({"error": "Student ID, name, and at least one class are required"}), 400
    db = get_db()
    valid_classes = db.execute(
        "SELECT id FROM classes WHERE id IN ({})".format(",".join("?" for _ in class_ids)),
        class_ids,
    ).fetchall()
    if len(valid_classes) != len(class_ids):
        db.close()
        return jsonify({"error": "Class not found"}), 404
    try:
        db.execute(
            "INSERT INTO students (id, name, class_id) VALUES (?, ?, ?)",
            (student_id, name, int(class_ids[0])),
        )
        db.commit()
    except sqlite3.IntegrityError:
        db.execute(
            "UPDATE students SET name = ?, class_id = ? WHERE id = ?",
            (name, int(class_ids[0]), student_id),
        )
        db.commit()
    for course_id in class_ids:
        db.execute(
            "INSERT OR IGNORE INTO student_courses (student_id, class_id) VALUES (?, ?)",
            (student_id, int(course_id)),
        )
    db.commit()
    db.close()
    return jsonify({"status": "saved"}), 201


@app.route("/api/students/bulk", methods=["POST"])
@teacher_required
def add_students_bulk():
    data = request.get_json(silent=True) or {}
    lines = str(data.get("lines", "")).strip().splitlines()
    class_ids = [str(value) for value in data.get("class_ids", []) if value is not None]
    if not lines or not class_ids:
        return jsonify({"error": "Classes and at least one student line are required"}), 400

    created = 0
    updated = 0
    errors = []
    db = get_db()
    valid_ids = {str(row["id"]) for row in db.execute(
        "SELECT id FROM classes WHERE id IN ({})".format(",".join("?" for _ in class_ids)),
        class_ids,
    ).fetchall()}
    if valid_ids != set(class_ids):
        db.close()
        return jsonify({"error": "One or more classes were not found"}), 404

    for line_number, line in enumerate(lines, start=1):
        if "," not in line:
            errors.append(f"Line {line_number}: use Student ID, Student Name")
            continue
        student_id, name = (part.strip() for part in line.split(",", 1))
        if not student_id or not name:
            errors.append(f"Line {line_number}: ID and name are required")
            continue
        existing = db.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
        if existing:
            db.execute(
                "UPDATE students SET name = ?, class_id = ? WHERE id = ?",
                (name, int(class_ids[0]), student_id),
            )
            updated += 1
        else:
            db.execute(
                "INSERT INTO students (id, name, class_id) VALUES (?, ?, ?)",
                (student_id, name, int(class_ids[0])),
            )
            created += 1
        for course_id in class_ids:
            db.execute(
                "INSERT OR IGNORE INTO student_courses (student_id, class_id) VALUES (?, ?)",
                (student_id, int(course_id)),
            )
    db.commit()
    db.close()
    return jsonify({"created": created, "updated": updated, "errors": errors}), 200

@app.route('/api/start_session', methods=['POST'])
@teacher_required
def start_session():
    data = request.get_json(silent=True) or {}
    class_id = data.get("class_id")
    if not class_id:
        return jsonify({"error": "class_id is required"}), 400
    try:
        class_id = int(class_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid class number"}), 400
    db = get_db()
    class_row = db.execute("SELECT id FROM classes WHERE id = ?", (class_id,)).fetchone()
    db.close()
    if not class_row:
        return jsonify({"error": "Class not found"}), 404
    current_session['code'] = "".join(secrets.choice("0123456789") for _ in range(6))
    current_session['class_id'] = class_id
    current_session['expires_at'] = time.time() + 1800
    current_session['present_students'] = []
    return jsonify({'code': current_session['code']})

@app.route('/api/mark_manual', methods=['POST'])
@teacher_required
def mark_manual():
    data = request.get_json(silent=True) or {}
    student_id = data.get("student_id")
    if not student_id:
        return jsonify({"error": "student_id is required"}), 400
    if student_id not in current_session['present_students']:
        current_session['present_students'].append(student_id)
        return jsonify({'status': 'success', 'action': 'added'})
    else:
        current_session['present_students'].remove(student_id)
        return jsonify({'status': 'success', 'action': 'removed'})


@app.route('/api/stop_session', methods=['POST'])
@teacher_required
def stop_session():
    current_session["code"] = None
    current_session["class_id"] = None
    current_session["expires_at"] = None
    current_session["present_students"] = []
    return jsonify({"status": "stopped"})

@app.route('/api/dashboard_data', methods=['GET'])
@teacher_required
def dashboard_data():
    class_id = current_session.get('class_id')
    if not class_id:
        return jsonify({'error': 'No active session'}), 400
    db = get_db()
    students_cursor = db.execute(
        '''SELECT students.id, students.name FROM students
           JOIN student_courses ON student_courses.student_id = students.id
           WHERE student_courses.class_id = ? ORDER BY students.name''',
        (class_id,),
    )
    full_roster = [{'id': row['id'], 'name': row['name']} for row in students_cursor.fetchall()]
    db.close()
    
    present_count = len(current_session['present_students'])
    total_count = len(full_roster)
    absent_count = total_count - present_count
    
    return jsonify({
        'present_count': present_count,
        'absent_count': absent_count,
        'total_count': total_count,
        'full_roster': full_roster,
        'present_ids': current_session['present_students']
    })

@app.route('/export/csv')
@teacher_required
def export_csv():
    if not current_session.get('class_id'):
        return "Error: No active session to export.", 400
    
    db = get_db()
    students_cursor = db.execute(
        '''SELECT students.id, students.name FROM students
           JOIN student_courses ON student_courses.student_id = students.id
           WHERE student_courses.class_id = ? ORDER BY students.name''',
        (current_session['class_id'],),
    )
    all_students = students_cursor.fetchall()
    db.close()
    
    csv_data = "StudentID,Name,Status\n"
    for student in all_students:
        status = 1 if student['id'] in current_session['present_students'] else 0
        csv_data += f"{student['id']},{student['name']},{status}\n"
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=attendance.csv"}
    )

if __name__ == '__main__':
    if not TEACHER_PASSWORD:
        print("TEACHER_PASSWORD is not set. Teacher dashboard login is disabled until it is configured.")
    app.run(debug=False, host="127.0.0.1", port=5000)
