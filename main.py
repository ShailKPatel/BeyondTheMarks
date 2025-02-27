import streamlit as st

# -------------------------------
# Streamlit Multi-Page Application Setup
# -------------------------------

# This script sets up a multi-page Streamlit application with a structured 
# navigation system. Each page serves a distinct purpose:
# 1. Home Page: Introduction and overview.
# 2. Data Dissector: Core analysis functionalities.
# 3. The Brains Behind: Credits for contributors.
# 4. Tech Wizardry: Technologies used in the project.

# Define views with corresponding file paths and icons

home = st.Page("views/Home.py", icon='🏠')  # Main landing page
data_dissector = st.Page("views/Data_Dissector.py", icon='🔬')  # Analysis & insights
the_brains_behind = st.Page("views/The_Brains_Behind.py", icon='🧠')  # Credits & acknowledgments
tech_wizardry = st.Page("views/Tech_Wizardry.py", icon='🛠️')  # Technologies used & dependencies
reviews = st.Page("views/reviews.py", icon='📨')  # Reviews

# -------------------------------
# Navigation Setup
# -------------------------------

# The `st.navigation()` function creates a structured menu where users can 
# navigate through different pages of the application. The keys in the dictionary 
# represent section names displayed in the navigation bar.

pg = st.navigation(
    [home,data_dissector,the_brains_behind,tech_wizardry,reviews]
)

# -------------------------------
# Run the Navigation System
# -------------------------------

# This method initializes the navigation system and ensures that the selected 
# page is displayed when the app runs. Each page file should contain its own 
# Streamlit logic and UI components.

pg.run()
