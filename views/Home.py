import streamlit as st

# Logo
image = "images/logo.png"
st.logo(image, size='large')

# ------------------------------------------------
# Home Page - Beyond The Marks
# ------------------------------------------------

# This script defines the home page for the Beyond The Marks.
# It provides an introduction, an overview of key features, and navigation
# to other views within the application.

# View Title
st.title("📊 Beyond The Marks 🎓")

# Subtitle & Description
st.markdown("""
Beyond The Marks processes academic records to uncover 
insights about student performance. It evaluates teacher effectiveness 
and detects possible biases based on gender or religion.  
This tool empowers institutions with data-driven decision-making.
""")

# -------------------------------
# Key Features
# -------------------------------

st.header("✨ Key Features")
st.markdown("""
✔ **File Validation & Parsing**: Supports CSV & Excel formats, ensuring correct data structure.  
✔ **Teacher Efficiency Analysis**: Uses **ANOVA** to assess teacher impact.  
✔ **Bias Detection**: Analyzes trends based on **gender** and **religion**.  
✔ **Student Performance Lookup**: Provides percentile-based insights.  
✔ **ANOVA for Teacher Evaluation**: Measuring the impact of teachers on student performance.  
✔ **One-Hot Encoding for Fairness**: Ensuring the model treats all labels equally.  
✔ **SHAP for Uncovering Bias**: Detecting hidden biases with explainable AI.
""")

# -------------------------------
# Navigation Links
# -------------------------------

st.header("📌 Explore the Tool")

with st.container(border=True):
    """ # Test Analysis Feature
    This page allows you to test the project and generate an analysis of student performance without uploading a file. If you prefer to test the app without providing your own data, you can use pre-existing analysis. To generate a synthetic analysis, simply click the button below.
    Generate detailed insights on student performance and trends."""
    st.page_link("views/View_Synthetic_Data.py", label="Generate Synthetic Analysis", icon="🧪")
with st.container(border=True):
    """ # 🔬 Data Analysis
    Generate detailed insights on student performance and trends."""
    st.page_link("views/Data_Analysis.py", label="Go to Data Analysis", icon="📊")

with st.container(border=True):
    """ # 🧠 The Brains Behind
    Meet the contributors who built this project."""
    st.page_link("views/The_Brains_Behind.py", label="View Contributors", icon="🧑")

with st.container(border=True):
    """ # 🛠️ Tech Wizardry
    Explore the technologies and tools that power this application."""
    st.page_link("views/Tech_Wizardry.py", label="View Technologies", icon="⚙️")

with st.container(border=True):
    """ # 📨 Reviews
    Got Complaint.. Er... Suggestion? Drop them here"""
    st.page_link("views/Reviews.py", label="Leave a Reviews", icon="📫")
    
with st.container(border=True):
    """ # 🎓 Attendance for Impact 
    An alternate to BeyondTheMarks analyzes subject-wise attendance-mark correlations, explains skewness, deviation, IQR, interprets trends, and suggests data-driven solutions for better performance."""
    st.link_button(url="https://attendance-for-impact.streamlit.app/", label="Try it", icon="🔀")

# -------------------------------
# Footer
# -------------------------------

st.markdown("---")
st.markdown("📜 **MIT Licensed** | 🚀 Developed for Educational Insights")

