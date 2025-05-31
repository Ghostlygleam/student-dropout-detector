import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from predictor import predict_dropout

st.set_page_config(page_title="Student Dropout Risk Detector", layout="wide")
st.title("🎓 Student Dropout Risk Detector")

# --- Connect to SQLite ---
DB_PATH = "students.db"

def get_all_students():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

def get_student_by_id(student_id):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM students WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def delete_student(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()

def add_student(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (
            Gender, Age, MaritalStatus, Course, AdmissionGrade, Scholarship,
            Debtor, FeesPaid, Sem1Enrolled, Sem1Approved, Sem1Grade,
            Sem2Enrolled, Sem2Approved, Sem2Grade
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(data.values()))
    conn.commit()
    conn.close()

# --- Navigation ---
option = st.sidebar.selectbox("📌 Menu", [
    "Add student manually", "Predict dropout (all)", "Predict by ID (with advice)", 
    "Search by ID", "View all students", "Delete student"
])


if option == "Add student manually":
    st.header("➕ Add New Student")
    gender = st.selectbox("Gender", {0: "Female", 1: "Male"}, format_func=lambda x: "Female" if x == 0 else "Male")
    age = st.slider("Age", 16, 40, 18)
    marital = st.selectbox("Marital Status", {1: "Single", 2: "Married", 3: "Divorced"}, format_func=lambda x: {1: "Single", 2: "Married", 3: "Divorced"}[x])
    course = st.selectbox("Course", ["Management", "Social Work", "Computer Science", "Design", "Journalism"])
    grade = st.slider("Admission Grade", 0.0, 200.0, 150.0)
    scholarship = st.selectbox("Scholarship", {0: "No", 1: "Yes"}, format_func=lambda x: "Yes" if x == 1 else "No")
    debtor = st.selectbox("Debtor", {0: "No", 1: "Yes"}, format_func=lambda x: "Yes" if x == 1 else "No")
    fees = st.selectbox("Fees Paid", {0: "No", 1: "Yes"}, format_func=lambda x: "Yes" if x == 1 else "No")
    sem1_enr = st.slider("1st Sem Enrolled", 0, 10, 5)
    sem1_app = st.slider("1st Sem Approved", 0, 10, 3)
    sem1_grade = st.slider("1st Sem Grade", 0.0, 20.0, 12.0)
    sem2_enr = st.slider("2nd Sem Enrolled", 0, 10, 5)
    sem2_app = st.slider("2nd Sem Approved", 0, 10, 3)
    sem2_grade = st.slider("2nd Sem Grade", 0.0, 20.0, 13.0)

    if st.button("Add Student"):
        new_student = {
            "Gender": gender,
            "Age": age,
            "MaritalStatus": marital,
            "Course": course,
            "AdmissionGrade": grade,
            "Scholarship": scholarship,
            "Debtor": debtor,
            "FeesPaid": fees,
            "Sem1Enrolled": sem1_enr,
            "Sem1Approved": sem1_app,
            "Sem1Grade": sem1_grade,
            "Sem2Enrolled": sem2_enr,
            "Sem2Approved": sem2_app,
            "Sem2Grade": sem2_grade
        }
        add_student(new_student)
        st.success("✅ Student added to database!")

elif option == "Predict dropout (all)":
    st.header("📊 Predict Dropout Risk")
    df = get_all_students()
    if df.empty:
        st.warning("No students in database.")
    else:
        prediction_input = df.drop(columns=["student_id"])
        predictions = predict_dropout(prediction_input)
        predictions["student_id"] = df["student_id"].values
        predictions = predictions.sort_values(by="Dropout (%)", ascending=False)
        st.dataframe(predictions)

        st.subheader("📈 Prediction Distribution")
        fig, ax = plt.subplots()
        predictions["Prediction"].value_counts().plot(kind="bar", color=["red", "orange", "green"], ax=ax)
        ax.set_ylabel("Number of Students")
        ax.set_xlabel("Prediction")
        st.pyplot(fig)

elif option == "Search by ID":
    st.header("🔍 Search Student by ID")
    student_id = st.number_input("Enter Student ID", min_value=1, step=1)
    if st.button("Search"):
        result = get_student_by_id(student_id)
        if not result.empty:
            st.dataframe(result)
        else:
            st.error("No student found with this ID.")

elif option == "Predict by ID (with advice)":
    st.header("🎯 Predict and Advise for One Student")
    student_id = st.number_input("Enter Student ID", min_value=1, step=1, key="predict_id")

    if st.button("Run Prediction", key="predict_one_btn"):
        df = get_student_by_id(student_id)

        if df.empty:
            st.error("No student found with this ID.")
        else:
            # Drop ID column and predict
            prediction_input = df.drop(columns=["student_id"])
            result_df = predict_dropout(prediction_input)
            result_df["student_id"] = student_id

            st.subheader("📊 Prediction result:")
            st.dataframe(result_df[["Prediction", "Dropout (%)", "Graduate (%)", "Enrolled (%)"]])

            st.subheader("📌 Advice:")

            risk = result_df.iloc[0]["Dropout (%)"]
            pred = result_df.iloc[0]["Prediction"]

            if risk >= 70:
                st.warning(f"🚨 High risk: {risk:.1f}% chance of dropout")
                st.markdown("- _Recommend academic counseling or mentor assignment._")

                if df.iloc[0]["Sem1Approved"] < 3 or df.iloc[0]["Sem2Approved"] < 3:
                    st.info("📉 Few approved subjects. Student might need extra academic support.")
            elif pred == "Graduate":
                st.success("🎓 Great! Student is on track to graduate.")
            else:
                st.info(f"🤔 Moderate risk. Keep monitoring student performance.")


elif option == "View all students":
    st.header("📋 All Students")
    df = get_all_students()
    if df.empty:
        st.warning("No students found.")
    else:
        st.dataframe(df)

elif option == "Delete student":
    st.header("🗑️ Delete Student by ID")
    student_id = st.number_input("Enter Student ID", min_value=1, step=1)
    if st.button("Delete"):
        delete_student(student_id)
        st.success(f"Student {student_id} deleted.")

# --- Admin panel / DB tools ---
st.markdown("## 🗂️ Database Tools")

with st.expander("🔍 Search Student by ID"):
    student_id = st.number_input("Enter Student ID", min_value=1, step=1, key="search_id")
    if st.button("Search", key="search_btn"):
        result = get_student_by_id(student_id)
        if not result.empty:
            st.success("Student found:")
            st.dataframe(result)
        else:
            st.error("Student not found.")

with st.expander("➕ Add New Student"):
    new_student = {}
    new_student["Gender"] = st.selectbox("Gender", [0, 1], key="new_gender")
    new_student["Age"] = st.slider("Age", 16, 40, 18, key="new_age")
    new_student["MaritalStatus"] = st.selectbox("Marital Status", [1, 2, 3], key="new_marital")
    new_student["Course"] = st.selectbox("Course", ["Management", "Social Work", "Informatics", "Design", "Journalism"], key="new_course")
    new_student["AdmissionGrade"] = st.slider("Admission Grade", 0.0, 200.0, 150.0, key="new_grade")
    new_student["Scholarship"] = st.selectbox("Scholarship", [0, 1], key="new_scholarship")
    new_student["Debtor"] = st.selectbox("Debtor", [0, 1], key="new_debtor")
    new_student["FeesPaid"] = st.selectbox("Fees Paid", [0, 1], key="new_fees")
    new_student["Sem1Enrolled"] = st.slider("1st Sem Enrolled", 0, 10, 5, key="new_sem1_enrolled")
    new_student["Sem1Approved"] = st.slider("1st Sem Approved", 0, 10, 3, key="new_sem1_approved")
    new_student["Sem1Grade"] = st.slider("1st Sem Grade", 0.0, 20.0, 12.0, key="new_sem1_grade")
    new_student["Sem2Enrolled"] = st.slider("2nd Sem Enrolled", 0, 10, 5, key="new_sem2_enrolled")
    new_student["Sem2Approved"] = st.slider("2nd Sem Approved", 0, 10, 3, key="new_sem2_approved")
    new_student["Sem2Grade"] = st.slider("2nd Sem Grade", 0.0, 20.0, 13.0, key="new_sem2_grade")

    if st.button("Add Student", key="add_btn_expander"):
        add_student(new_student)
        st.success("✅ Student added successfully!")

with st.expander("🗑️ Delete Student by ID"):
    del_id = st.number_input("Enter Student ID to delete", min_value=1, step=1, key="delete_id")
    if st.button("Delete", key="delete_btn"):
        delete_student(del_id)
        st.warning(f"Student with ID {del_id} deleted.")

