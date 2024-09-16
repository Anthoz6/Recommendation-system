import sqlite3

def create_database():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    # Crear tabla para cursos recomendados con imágenes y URL
    c.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career TEXT NOT NULL,
        course TEXT NOT NULL,
        image_url TEXT
    )
    ''')

    # Crear tabla para historial de interacciones
    c.execute('''
    CREATE TABLE IF NOT EXISTS interaction_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    print("Database and tables created successfully.") 

    conn.commit()
    conn.close()

def add_course_to_db(career, course, image_url, course_url):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    c.execute('''
    INSERT INTO courses (career, course, image_url, course_url)
    VALUES (?, ?, ?, ?)
    ''', (career, course, image_url, course_url))

    conn.commit()
    conn.close()

def add_interaction(student_id, course_id):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    c.execute('''
    INSERT INTO interaction_history (student_id, course_id)
    VALUES (?, ?)
    ''', (student_id, course_id))

    conn.commit()
    conn.close()

def get_courses_for_career(career):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    c.execute('''
    SELECT course, image_url FROM courses WHERE career = ?
    ''', (career,))

    courses = c.fetchall()
    conn.close()
    return courses

def get_all_courses():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    c.execute('''
    SELECT course, image_url FROM courses
    ''')

    courses = c.fetchall()
    conn.close()
    return courses

def get_course_by_id(course_id):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    c.execute('''
    SELECT course, image_url FROM courses WHERE id = ?
    ''', (course_id,))

    course = c.fetchone()
    conn.close()
    return course

def get_user_interactions(student_id):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    c.execute('''
    SELECT course_id FROM interaction_history WHERE student_id = ?
    ''', (student_id,))

    interactions = c.fetchall()
    conn.close()
    return interactions

import sqlite3

# Función para eliminar un curso de la base de datos por nombre o ID
def delete_course(course_id=None, course_name=None):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    # Verificar si se pasa un ID de curso o un nombre
    if course_id:
        c.execute('DELETE FROM courses WHERE id = ?', (course_id,))
    elif course_name:
        c.execute('DELETE FROM courses WHERE course = ?', (course_name,))
    else:
        raise ValueError("Se debe proporcionar un ID o un nombre de curso para eliminar.")

    conn.commit()
    conn.close()
