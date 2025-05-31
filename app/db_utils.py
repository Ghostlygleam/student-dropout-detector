import sqlite3
import pandas as pd

DB_NAME = "students.db"

def connect():
    return sqlite3.connect(DB_NAME)

def get_all_students():
    conn = connect()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

def get_student_by_id(student_id):
    conn = connect()
    df = pd.read_sql(f"SELECT * FROM students WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def add_student(student_data):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (
            Gender, Age, MaritalStatus, Course, AdmissionGrade,
            Scholarship, Debtor, FeesPaid,
            Sem1Enrolled, Sem1Approved, Sem1Grade,
            Sem2Enrolled, Sem2Approved, Sem2Grade
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, student_data)
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
