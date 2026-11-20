import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="Student Dashboard", layout="wide")

# Dashboard title
st.title("🎓 Student Performance Dashboard")
st.write("Analyze student marks and academic performance")

# Load dataset
df = pd.read_csv("student-mat.csv", sep=";")

# Sidebar filters
st.sidebar.header("Filters")

school_list = ["All"] + list(df["school"].unique())
selected_school = st.sidebar.selectbox("Select School", school_list)

sex_list = ["All"] + list(df["sex"].unique())
selected_sex = st.sidebar.selectbox("Select Gender", sex_list)

# Apply filters
filtered_df = df.copy()

if selected_school != "All":
    filtered_df = filtered_df[filtered_df["school"] == selected_school]

if selected_sex != "All":
    filtered_df = filtered_df[filtered_df["sex"] == selected_sex]

# Calculate metrics
total_students = len(filtered_df)
average_grade = filtered_df["G3"].mean()
passed_students = len(filtered_df[filtered_df["G3"] >= 10])
failed_students = len(filtered_df[filtered_df["G3"] < 10])

pass_percentage = (
    (passed_students / total_students) * 100
    if total_students > 0 else 0
)

# Display metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("Average Final Grade", round(average_grade, 2) if total_students else 0)
col3.metric("Passed Students", passed_students)
col4.metric("Pass Percentage", f"{pass_percentage:.1f}%")

st.divider()

# Pass and Fail chart
st.subheader("📊 Pass vs Fail Students")

pass_fail_data = pd.DataFrame({
    "Result": ["Pass", "Fail"],
    "Students": [passed_students, failed_students]
})

fig1 = px.pie(
    pass_fail_data,
    names="Result",
    values="Students",
    title="Pass/Fail Distribution",
    hole=0.4
)

st.plotly_chart(fig1, use_container_width=True)

# Grade analysis
st.subheader("📈 Grade Analysis")

grade_data = pd.DataFrame({
    "Exam": ["First Grade (G1)", "Second Grade (G2)", "Final Grade (G3)"],
    "Average Marks": [
        filtered_df["G1"].mean(),
        filtered_df["G2"].mean(),
        filtered_df["G3"].mean()
    ]
})

fig2 = px.bar(
    grade_data,
    x="Exam",
    y="Average Marks",
    title="Average Marks in Exams",
    text_auto=True
)

st.plotly_chart(fig2, use_container_width=True)

# Student performance scatter plot
st.subheader("📚 Student Performance Comparison")

fig3 = px.scatter(
    filtered_df,
    x="G1",
    y="G3",
    color="sex",
    title="First Exam Marks vs Final Marks",
    labels={
        "G1": "First Exam Marks",
        "G3": "Final Exam Marks",
        "sex": "Gender"
    }
)

st.plotly_chart(fig3, use_container_width=True)

# Dataset table
st.subheader("📋 Student Dataset")

st.dataframe(filtered_df, use_container_width=True)

# Download filtered data
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Student Data",
    data=csv_data,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")