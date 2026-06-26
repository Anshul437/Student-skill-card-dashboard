from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "skillcard"

# ---------------- DATABASE ----------------

def init_db():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            name TEXT,
            skill TEXT,
            marks INTEGER
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template('index.html')

# ---------------- TEACHER ----------------

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        skill = request.form['skill']
        marks = request.form['marks']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute('''
            INSERT INTO students
            (username, password, name, skill, marks)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, name, skill, marks))

        conn.commit()
        conn.close()

        return redirect('/teacher')

    return render_template('teacher.html')

# ---------------- STUDENT LOGIN ----------------

@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute('''
            SELECT * FROM students
            WHERE username=? AND password=?
        ''', (username, password))

        student = cur.fetchone()

        conn.close()

        if student:
            session['student_id'] = student[0]
            return redirect('/dashboard')

    return render_template('studentlogin.html')

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    if 'student_id' not in session:
        return redirect('/studentlogin')

    student_id = session['student_id']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cur.fetchone()

    conn.close()

    return render_template('dashboard.html', student=student)

# ---------------- ALL STUDENTS ----------------

@app.route('/student')
def student():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template('student.html', students=students)

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(debug=True) 