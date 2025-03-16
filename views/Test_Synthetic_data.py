import streamlit as st
import pandas as pd
import core_functionality.data_validator as dv
import analysis.teacher_analysis as ta
import analysis.subject_analysis as sa
import bias_analysis.bias_detection as bd
import io

# Logo
image = "images/logo.png"
st.logo(image, size='large')

# -------------------------------
# Title & File Upload Section
# -------------------------------
# methods

st.title("🔬 Data Dissection: Where Numbers Spill Their Secrets!")

synthetic_data = pd.read_csv("samplefiles/test4.csv")  # Load synthetic data
csv_buffer = io.StringIO()  # Create an in-memory file object
synthetic_data.to_csv(csv_buffer, index=False)  # Write DataFrame to this buffer
csv_buffer.seek(0)  # Move to the beginning of the buffer
marksheet = csv_buffer  # Assign as a file-like object
marksheet.name = "synthetic_data.csv"  # Mimic UploadedFile behavior


st.page_link("views/Data_Analysis.py", label="Try it with your own data!", icon="🔁")    
    
if marksheet is not None:

    # Determine file type and read accordingly
    try:
        df, subject_names = dv.validate_and_convert_file(marksheet)
        st.write(df)
        st.success("Nice! We are working with sample data! 📊")
        has_error = False

        

    except Exception as e:
        st.error(f"You didn't read the `The Grand Data Upload Rulebook 📜`: {e}.\nTry reloading page")
        st.write(e.__traceback__)
        has_error = True



# -------------------------------
# Analysis Options with Witty Labels
# -------------------------------
if marksheet and not has_error:
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

            if fig1: 
                st.plotly_chart(fig1)  # Show correlation matrix
            if fig2: 
                st.plotly_chart(fig2)  # Show box plot
            
            for fig in scatter_list:
                st.plotly_chart(fig)  # Show each scatter plot


    except TypeError as e:
        st.error(f"You didn't read the `The Grand Data Upload Rulebook 📜`: {e}.\nTry reloading page")


# -------------------------------
# Fun Closing Line
# -------------------------------

st.markdown("☕ *Made with Caffine*")

