import streamlit as st
import pandas as pd
import core_functionality.data_validator as dv
import analysis.teacher_analysis as ta
import analysis.subject_analysis as sa
import bias_analysis.bias_detection as bd

# Logo
image = "images/logo.png"
st.logo(image, size='large')

# -------------------------------
# Title & File Upload Section
# -------------------------------
# methods

st.title("🔬 Data Dissection: Where Numbers Spill Their Secrets!")

st.subheader("📂 Upload Your 'Highly Confidential' Marksheet")
marksheet = False


marksheet = st.file_uploader("Upload Combined Marksheet (CSV, XLS, XLSX)", type=["csv", "xls", "xlsx"])

if marksheet:

    # Determine file type and read accordingly
    try:
        df, subject_names = dv.validate_and_convert_file(marksheet)
        st.write(df)
        st.success("Nice! Your file is in—time to dig into the academic drama! 📊")
        
        

    except Exception as e:
        st.error(f"You didn't read the `The Grand Data Upload Rulebook 📜`: {e}")
        
# Data Upload Rulebook
if not marksheet:
    st.markdown("""
    ### 🚨 **The Grand Data Upload Rulebook 📜** 🚨  

    Ah, dear uploader, you dare challenge the mighty gates of **Data Validation?** Fear not! Follow these sacred rules, and your file shall pass. Break them, and your data shall be cast into the abyss of rejection!  

    ---

    ### ✅ **Allowed File Formats:**  
    📂 **.csv** – The spreadsheet superhero.  
    📂 **.xls, .xlsx, .xlsm, .xlsb** – The Excel empire (Yes, even `.xlsb`, the mysterious one).  

    🚫 **Forbidden Formats:** **.txt, .pdf, .png, .jpg, .docx, .pptx** (We analyze numbers, not ransom notes or abstract art).  

    ---

    ### 📏 **Structural Laws of the Data Universe**  

    🆔 **Roll No:** The sacred identifier—must be unique! No duplicates, no missing values, no nonsense!  

    📊 **Subject Columns:**  
    ✔ Format: **[Subject] Attendance** and **[Subject] Marks** (e.g., "Math Attendance", "Math Marks").  
    ✔ If an attendance column exists for a subject, the marks **MUST** also exist (and vice versa). No lone rangers!  

    👨‍🏫 **Teacher Column (Optional, but respected)**  
    ✔ If present, should follow the **"[Subject] Teacher"** format (e.g., "Math Teacher").  
    ✔ If missing, we assume **all teachers are omnipresent beings.**  

    ---

    ### 🔢 **Numerical Discipline**  
    ✔ **Attendance & Marks:** Must be numeric (0 to 100). No alphabets, emojis, or secret codes!  
    ✔ **Rounded to 2 decimal places.** This isn’t quantum physics; we don’t need 27 decimal points.  

    ---

    ### 🚧 **Limits & Restrictions**  
    🛑 **Maximum** of **N subjects** allowed. This isn’t Hogwarts; you can’t study infinite subjects!  
    🛑 **Unexpected columns will be exiled!** If it's not Roll No, Attendance, Marks, or Teacher, we don’t want it.  

    ---

    ### ⚠ **Final Warning**  
    Break these rules, and your file shall face:  
    ❌ Instant rejection  
    ❌ Merciless error messages  
    ❌ A disappointed AI staring at you 😐  

    Follow them, and your data shall pass the validation gates with glory! 🎉  
    """)
    
# -------------------------------
# Analysis Options with Witty Labels
# -------------------------------
if marksheet:
    st.subheader("🔍 Pick Your Investigation Mode:")
    try:

        if st.button("📚 Professor Performance Analyzation"):
            
            # Step 1: Extract subjects with teachers
            teacher_subjects = [subj for subj in subject_names if f"{subj} Teacher" in df.columns]

            teacher_scores = {}  # Dictionary to store scores for each teacher
            
            teacher_score_df = {}

            # Step 2: Loop through subjects that have a teacher column
            for subject in teacher_subjects:
                teacher_col = f"{subject} Teacher"
                attendance_col = f"{subject} Attendance"
                marks_col = f"{subject} Marks"

                # Ensure required columns exist
                if attendance_col in df.columns and marks_col in df.columns:
                    # Step 3: Create a DataFrame with Teacher, Attendance, and Marks
                    teacher_df = df[[teacher_col, attendance_col, marks_col]].dropna()
                    # Step 4: Compute Teacher Score
                    teacher_scores[subject] = ta.analyze_teacher_effectiveness(teacher_df)
                    # Step 5: Display Teacher Scores Matrix
                    # Check if all subjects contain empty data
                    can_be_predicted = True
                    if all(all(not v for v in subject_data.values()) for subject_data in teacher_scores.values()):
                        can_be_predicted = False
                    else:
                        # Convert dictionary to a proper DataFrame
                        formatted_data = []
                        
                        for subject, subject_data in teacher_scores.items():
                            for category, teacher_dict in subject_data.items():  # 'Marks' and 'Attendance'
                                for teacher, score in teacher_dict.items():
                                    formatted_data.append({
                                        "Subject": subject,
                                        "Teacher": teacher,
                                        "Category": category,
                                        "Score": round(score, 2)  # Keep 2 decimal places
                                    })

                        # Convert list to DataFrame
                        teacher_score_df = pd.DataFrame(formatted_data)

                    # Graph
                    st.subheader(f"Teacher Performance Analysis for {subject}")
                    teacher_df = teacher_df.rename(columns={f"{subject} Teacher": "Teacher"})
                    teacher_df = teacher_df.rename(columns={f"{subject} Attendance": "Attendance"})
                    teacher_df = teacher_df.rename(columns={f"{subject} Marks": "Marks"})
                    attendance_fig, marks_fig = ta.plot_teacher_distributions(teacher_df)

                    st.plotly_chart(attendance_fig)
                    st.plotly_chart(marks_fig)
                        
                    # Step 6: Plot Teacher Distributions
                    if not can_be_predicted:
                        st.subheader(f"Performance Distribution for {subject} Teachers")
                        st.write("You don't have enough data to give scores to teachers!")
                    # ta.plot_teacher_distributions(teacher_df)
            
            # Display in matrix format using pivot
            if can_be_predicted:
                teacher_score_pivot = teacher_score_df.pivot(index=["Subject", "Teacher"], columns="Category", values="Score")
                st.subheader("📊 Teacher Score Matrix")
                st.dataframe(teacher_score_pivot)
                
                
        if st.button("⚖️ Gender Bias Detection"):
            if 'Gender' not in df.columns:
                st.write("🚨 Whoops! Your data doesn't have a 'Gender' column! 🤦‍♂️")
                st.write("Analyzing gender bias without gender is like judging a cricket match without knowing the teams. 🏏")
            else:
                for subject in subject_names:
                    attendance_col = f"{subject} Attendance"
                    marks_col = f"{subject} Marks"
                    teacher_col = f"{subject} Teacher" if f"{subject} Teacher" in df.columns else None

                    if attendance_col not in df.columns or marks_col not in df.columns:
                        st.write(f"⚠️ Skipping {subject}: Missing necessary columns!")
                    else:
                        # Prepare DataFrame slice
                        cols_to_use = [attendance_col, marks_col, "Gender"]
                        if teacher_col:
                            cols_to_use.append(teacher_col)

                        subject_df = df[cols_to_use]

                        # Call the bias detection method
                        st.write(f"🔍 Running bias detection for {subject}...")
                        st.plotly_chart(bd.detect_bias(subject_df))

                st.write("✅ Bias analysis complete! If the results make you uncomfortable, welcome to reality. 😉")


        if st.button("☪️✝️🕉️ Religious Bias Detection"):
            if 'Religion' not in df.columns:
                st.write("🙏 Oh no! Your data doesn't have a 'Religion' column! 😇")
                st.write("Trying to analyze religious bias without religion is like arguing about food without knowing what's on the plate. 🍛")
            else:
                for subject in subject_names:
                    attendance_col = f"{subject} Attendance"
                    marks_col = f"{subject} Marks"
                    teacher_col = f"{subject} Teacher" if f"{subject} Teacher" in df.columns else None

                    if attendance_col not in df.columns or marks_col not in df.columns:
                        st.write(f"⚠️ Skipping {subject}: Missing necessary columns! Maybe the data needs a divine intervention. ✨")
                    else:
                        # Prepare DataFrame slice
                        cols_to_use = [attendance_col, marks_col, "Religion"]
                        if teacher_col:
                            cols_to_use.append(teacher_col)

                        subject_df = df[cols_to_use]

                        # Call the bias detection method
                        st.write(f"🔍 Running religious bias detection for {subject}... 🙏")
                        st.plotly_chart(bd.detect_bias(subject_df))

                st.write("✅ Bias analysis complete! If the results are shocking, just remember—faith can move mountains, but data doesn’t lie. 📊😉")


        if st.button("📊 Subject Showdown: Which One Wins?"):
            fig1, fig2, scatter_list = sa.analyze_subject_performance(df, subject_names)

            if fig1: st.plotly_chart(fig1)  # Show correlation matrix
            if fig2: st.plotly_chart(fig2)  # Show box plot
            
            for fig in scatter_list:
                st.plotly_chart(fig)  # Show each scatter plot


    except TypeError as e:
        st.error(f"You didn't read the `The Grand Data Upload Rulebook 📜`: {e}")


# -------------------------------
# Fun Closing Line
# -------------------------------

st.markdown("☕ *Made with Caffine*")


