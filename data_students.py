import sqlite3

def create_student_database():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    # Crear tabla para estudiantes
    c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        career TEXT NOT NULL
    )
    ''')

    print("Student database and table created successfully.")

    conn.commit()
    conn.close()

def add_student(name, career):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    c.execute('''
    INSERT INTO students (name, career)
    VALUES (?, ?)
    ''', (name, career))

    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    c.execute('''
    SELECT id, name, career FROM students
    ''')

    students = c.fetchall()
    conn.close()
    return students
