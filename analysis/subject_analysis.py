import pandas as pd
import plotly.express as px
import statsmodels.api as sm

def analyze_subject_performance(df, subject_names):
    """
    Analyzes subject-wise performance based on marks and attendance.

    Args:
        df (pd.DataFrame): The main dataset containing student performance details.
        subject_names (list): List of subject names (e.g., ["Math", "Science", "English"]).

    Returns:
        tuple: (correlation_matrix_fig, subject_marks_boxplot, attendance_vs_marks_scatter_list)
            - Correlation Matrix Heatmap (Plotly) or None if only one subject.
            - Box Plot of Subject Marks (Plotly) or None if only one subject.
            - List of Scatter Plots (one per subject) showing Attendance vs. Marks with regression line.
    """

    # Default to None for correlation matrix and box plot
    correlation_matrix_fig = None
    subject_marks_boxplot = None

    # 1️⃣ CORRELATION MATRIX (Heatmap)
    if len(subject_names) > 1:
        # Extract only marks columns for correlation analysis
        marks_df = df[[f"{sub} Marks" for sub in subject_names]]
        correlation_matrix = marks_df.corr()

        correlation_matrix_fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            labels=dict(color="Correlation"),
            title="Subject Marks Correlation Matrix",
            color_continuous_scale="viridis",
        )

    # 2️⃣ BOX PLOT OF SUBJECT-WISE MARKS
    if len(subject_names) > 1:
        # Convert marks columns to long format for Plotly
        marks_long_df = df.melt(id_vars=["Roll No", "Name"], 
                                value_vars=[f"{sub} Marks" for sub in subject_names], 
                                var_name="Subject", 
                                value_name="Marks")

        marks_long_df["Subject"] = marks_long_df["Subject"].str.replace(" Marks", "")

        subject_marks_boxplot = px.box(
            marks_long_df,
            x="Subject",
            y="Marks",
            title="Distribution of Marks Across Subjects",
            color="Subject"
        )

    # 3️⃣ SCATTER PLOTS (Attendance vs. Marks per Subject)
    scatter_plots = []

    for subject in subject_names:
        # Extract attendance and marks for the subject
        attendance_col = f"{subject} Attendance"
        marks_col = f"{subject} Marks"

        # Fit a simple linear regression model
        X = df[attendance_col].astype(float)
        y = df[marks_col].astype(float)

        X = sm.add_constant(X)  # Add intercept for OLS regression
        model = sm.OLS(y, X).fit()

        # Extract regression parameters
        intercept = model.params[0]  # Constant (c)
        slope = model.params[1]  # Coefficient of attendance (m)

        # Print regression equation
        print(f"{subject}: Marks = {slope:.2f} × Attendance + {intercept:.2f}")

        # Create scatter plot with regression line
        scatter_plot = px.scatter(
            df,
            x=attendance_col,
            y=marks_col,
            title=f"{subject}: Attendance vs. Marks",
            trendline="ols",
            labels={attendance_col: "Attendance (%)", marks_col: "Marks"}
        )

        # Annotate full equation on the plot
        scatter_plot.add_annotation(
            x=df[attendance_col].max(), 
            y=df[marks_col].max(),
            text=f"Marks = {slope:.2f} × Attendance + {intercept:.2f}",
            showarrow=False,
            font=dict(size=14, color="red")
        )

        scatter_plots.append(scatter_plot)

    return correlation_matrix_fig, subject_marks_boxplot, scatter_plots

if __name__ == "__main__":
    # Sample dataset
    data = {
        "Roll No": [1, 2, 3, 4, 5],
        "Name": ["Amit", "Neha", "Rohan", "Sara", "Vikram"],
        "Math Marks": [85, 78, 92, 65, 80],
        "Math Attendance": [90, 85, 95, 60, 88],
        "Science Marks": [75, 88, 79, 72, 85],
        "Science Attendance": [80, 92, 78, 85, 90],
        "English Marks": [82, 79, 88, 77, 83],
        "English Attendance": [85, 80, 90, 70, 82],
    }

    df = pd.DataFrame(data)

    # Test with multiple subjects
    subjects = ["Math", "Science", "English"]
    fig1, fig2, scatter_list = analyze_subject_performance(df, subjects)

    if fig1: fig1.show()  # Show correlation matrix
    if fig2: fig2.show()  # Show box plot

    for fig in scatter_list:
        fig.show()  # Show each scatter plot

    # Test with a single subject
    print("\nTesting with a single subject...\n")
    single_subject = ["Math"]
    fig1, fig2, scatter_list = analyze_subject_performance(df, single_subject)

    print(fig1, fig2)  # Should print: None, None

    for fig in scatter_list:
        fig.show()  # Scatter plot should still be shown
