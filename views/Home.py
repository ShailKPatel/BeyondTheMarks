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
_A smart data-driven tool designed to analyze student performance, 
evaluate teacher effectiveness, and detect potential biases._  
""")

# -------------------------------
# Project Overview
# -------------------------------

st.header("🔍 Overview")
st.write("""
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
✔ **3D Data Visualization**: Plots **attendance vs. theory vs. practical marks**.  
✔ **Error Handling**: Custom exceptions for invalid files, missing data, and format issues.  
""")

# -------------------------------
# Navigation Links
# -------------------------------

st.header("📌 Explore the Tool")

with st.container(border=True):
    """ # 🔬 Data Dissector
    Generate detailed insights on student performance and trends."""
    st.page_link("views/Data_Dissector.py", label="Go to Data Dissector", icon="📊")

with st.container(border=True):
    """ # 🧠 The Brains Behind
    Meet the contributors who built this project."""
    st.page_link("views/The_Brains_Behind.py", label="View Contributors", icon="🧑")

with st.container(border=True):
    """ # 🛠️ Tech Wizardry
    Explore the technologies and tools that power this application."""
    st.page_link("views/Tech_Wizardry.py", label="View Technologies", icon="⚙️")

with st.container(border=True):
    """ # 🛠️ Reviews
    Got Complaint.. Er... Suggestion? Drop them here"""
    st.page_link("views/Reviews.py", label="Leave a Reviews", icon="⚙️")

# -------------------------------
# Footer
# -------------------------------

st.markdown("---")
st.markdown("📜 **MIT Licensed** | 🚀 Developed for Educational Insights")

