import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Drop table if it exists (for debugging/demo purposes)
cursor.execute("DROP TABLE IF EXISTS students")

# Create the table
cursor.execute("""
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Gender INTEGER,
    Age INTEGER,
    MaritalStatus INTEGER,
    Course TEXT,
    AdmissionGrade REAL,
    Scholarship INTEGER,
    Debtor INTEGER,
    FeesPaid INTEGER,
    Sem1Enrolled INTEGER,
    Sem1Approved INTEGER,
    Sem1Grade REAL,
    Sem2Enrolled INTEGER,
    Sem2Approved INTEGER,
    Sem2Grade REAL
)
""")

# Sample students to insert
sample_students = [
    (0, 18, 1, "Management", 145.5, 1, 0, 1, 7, 5, 13.0, 6, 4, 14.2),
    (1, 22, 2, "Computer Science", 160.0, 0, 1, 0, 8, 3, 11.0, 8, 2, 10.5),
    (0, 19, 1, "Design", 130.0, 1, 0, 1, 6, 4, 14.8, 5, 3, 15.0),
    (1, 25, 3, "Social Work", 120.0, 0, 1, 0, 5, 2, 9.5, 6, 1, 8.0),
    (0, 20, 2, "Journalism", 180.0, 1, 0, 1, 9, 7, 16.0, 8, 6, 17.0)
]

# Insert into the table
cursor.executemany("""
INSERT INTO students (
    Gender, Age, MaritalStatus, Course, AdmissionGrade, Scholarship,
    Debtor, FeesPaid, Sem1Enrolled, Sem1Approved, Sem1Grade,
    Sem2Enrolled, Sem2Approved, Sem2Grade
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sample_students)

conn.commit()
conn.close()
print("✅ Database created and populated with sample students.")
