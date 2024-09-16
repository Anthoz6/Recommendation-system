import sqlite3

conn = sqlite3.connect('courses.db')
c = conn.cursor()

c.execute("PRAGMA table_info(courses);")
columns = c.fetchall()
print("Columnas actuales en la tabla 'courses':")
for column in columns:
    print(column)

conn.close()
