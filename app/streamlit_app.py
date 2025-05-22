import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from predictor import predict_dropout

st.set_page_config(page_title="Dropout Risk Detector", layout="wide")
st.title("🎓 Student Dropout Risk Detector")

# --- Input method: CSV or manual ---
mode = st.radio("📥 Select input method", ["Upload CSV", "Enter manually"])

if mode == "Upload CSV":
    uploaded_file = st.file_uploader("📂 Upload a CSV file with student data (without target column)", type=["csv"])

    if uploaded_file:
        try:
            input_df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            input_df = None
    else:
        input_df = None

else:
    st.subheader("🧾 Enter 15 Features")

    gender = st.selectbox("Gender", {0: "Female", 1: "Male"}, format_func=lambda x: "Female" if x == 0 else "Male")
    age = st.slider("Age at enrollment", 16, 40, 18)
    marital_status = st.selectbox("Marital status", {1: "Single", 2: "Married", 3: "Divorced"}, format_func=lambda x: {1: "Single", 2: "Married", 3: "Divorced"}[x])
    course = st.selectbox("Study program", ["Management", "Social Work", "Computer Science", "Design", "Journalism"])
    admission_grade = st.slider("Admission grade", 0.0, 200.0, 150.0)
    scholarship = st.selectbox("Scholarship holder", {0: "No", 1: "Yes"}, format_func=lambda x: "Yes" if x == 1 else "No")
    debtor = st.selectbox("Has debt", {0: "No", 1: "Yes"}, format_func=lambda x: "Yes" if x == 1 else "No")
    fees_paid = st.selectbox("Tuition fees up to date", {0: "No", 1: "Yes"}, format_func=lambda x: "Yes" if x == 1 else "No")

    st.markdown("### 📚 1st Semester")
    sem1_enrolled = st.slider("Subjects enrolled", 0, 10, 5)
    sem1_approved = st.slider("Subjects approved", 0, 10, 3)
    sem1_grade = st.slider("Average grade", 0, 20, 12)

    st.markdown("### 📚 2nd Semester")
    sem2_enrolled = st.slider("Subjects enrolled", 0, 10, 5, key="sem2_enrolled")
    sem2_approved = st.slider("Subjects approved", 0, 10, 3, key="sem2_approved")
    sem2_grade = st.slider("Average grade", 0, 20, 13, key="sem2_grade")

    input_df = pd.DataFrame([{
        "Gender": gender,
        "Age at enrollment": age,
        "Marital Status": marital_status,
        "Course": course,
        "Admission grade": admission_grade,
        "Scholarship holder": scholarship,
        "Debtor": debtor,
        "Tuition fees up to date": fees_paid,
        "Curricular units 1st sem (enrolled)": sem1_enrolled,
        "Curricular units 1st sem (approved)": sem1_approved,
        "Curricular units 1st sem (grade)": sem1_grade,
        "Curricular units 2nd sem (enrolled)": sem2_enrolled,
        "Curricular units 2nd sem (approved)": sem2_approved,
        "Curricular units 2nd sem (grade)": sem2_grade
    }])

# --- Main logic if data exists ---
if input_df is not None and not input_df.empty:
    result_df = predict_dropout(input_df)

    # Sort by dropout risk
    result_df = result_df.sort_values(by="Dropout (%)", ascending=False)

    st.subheader("📊 Prediction results:")
    st.dataframe(result_df[["Prediction", "Dropout (%)", "Graduate (%)", "Enrolled (%)"]])

    # Warning for high-risk students
    st.subheader("⚠️ Students at high dropout risk (≥ 70%):")
    high_risk_df = result_df[result_df["Dropout (%)"] >= 70]

    if not high_risk_df.empty:
        st.warning(f"🚨 {len(high_risk_df)} students identified with high dropout risk!")
        for i, row in high_risk_df.iterrows():
            st.markdown(f"- **Student {i+1}**: {row['Dropout (%)']}% — _counseling and academic support recommended_.")
            if row['Curricular units 1st sem (approved)'] < 3 or row['Curricular units 2nd sem (approved)'] < 3:
                st.info("Reason: low number of approved subjects. Suggest assigning an academic mentor.")
    else:
        st.success("🎉 No students with dropout risk ≥ 70%!")

    # Distribution chart
    st.subheader("📈 Prediction distribution:")
    fig, ax = plt.subplots()
    result_df["Prediction"].value_counts().plot(kind="bar", color=["red", "orange", "green"], ax=ax)
    ax.set_ylabel("Number of students")
    ax.set_xlabel("Prediction category")
    st.pyplot(fig)

