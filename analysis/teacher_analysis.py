from scipy.stats import f_oneway
import pandas as pd
from scipy.stats import iqr
import plotly.express as px
import streamlit as st


def anova_significance(df):
    """
    Performs a one-way ANOVA test to check if there is a significant difference 
    in the given metric (either Marks or Attendance) across different teachers.

    Args:
    df (pd.DataFrame): A DataFrame containing exactly two columns:
            - One "Teacher" column (e.g., "Math Teacher").
            - One numerical column (either "Marks" or "Attendance").
    
    Returns:
    bool: True if the ANOVA test finds a significant difference (p-value < 0.1), 
            otherwise False.
    
    Raises:
    ValueError: If the DataFrame does not have exactly two columns, 
                or if the second column is not numeric.
    """
    
    # Ensure DataFrame has exactly 2 columns
    if df.shape[1] != 2:
        raise ValueError("DataFrame must contain exactly two columns: 'Teacher' and a numeric column.")

    # Identify the teacher column and numeric column dynamically
    teacher_col = [col for col in df.columns if "Teacher" in col][0]
    value_col = [col for col in df.columns if col != teacher_col][0]

    # Ensure the numeric column contains valid numerical data
    if not pd.api.types.is_numeric_dtype(df[value_col]):
        raise ValueError(f"Column '{value_col}' must be numeric.")

    # Group data by teacher and extract the values for ANOVA
    groups = [group[value_col].values for _, group in df.groupby(teacher_col)]

    # ANOVA requires at least two groups to compare
    if len(groups) < 2:
        return False  # Not enough data to perform ANOVA

    # Perform one-way ANOVA test
    _, p_value = f_oneway(*groups)

    # Return True if the p-value is less than 0.1 (statistically significant difference)
    return p_value < 0.1

def calculate_teacher_mean(df):
    """
    Calculates the mean of the numeric column for each teacher.

    Args:
    df (pd.DataFrame): A DataFrame with two columns: 'Teacher' and a numeric column (Marks/Attendance).

    Returns:
    dict: A dictionary with teacher names as keys and their respective means as values.
    """
    teacher_col = [col for col in df.columns if "Teacher" in col][0]
    value_col = [col for col in df.columns if col != teacher_col][0]

    return df.groupby(teacher_col)[value_col].mean().to_dict()

def calculate_teacher_iqr(df):
    """
    Calculates the Interquartile Range (IQR) of the numeric column for each teacher.

    Args:
    df (pd.DataFrame): A DataFrame with two columns: 'Teacher' and a numeric column (Marks/Attendance).

    Returns:
    dict: A dictionary with teacher names as keys and their respective IQR values as values.
    """
    teacher_col = [col for col in df.columns if "Teacher" in col][0]
    value_col = [col for col in df.columns if col != teacher_col][0]

    return df.groupby(teacher_col)[value_col].apply(iqr).to_dict()

def analyze_teacher_effectiveness(df):
    """
    Analyzes teacher effectiveness by checking if there is a significant difference 
    in both Attendance and Marks across teachers using ANOVA.
    If significant, calculates a teacher score based on Mean (0.6) and IQR (0.4).
    A teacher must have more than or euqal to 3 students to be analyzed.

    Args:
    df (pd.DataFrame): A DataFrame with at least three columns: 
                one 'Teacher' column and two numeric columns ('Marks' and 'Attendance').

    Returns:
    dict: A dictionary containing two sub-dictionaries:
            - 'Marks': {teacher_name: effectiveness_score}
            - 'Attendance': {teacher_name: effectiveness_score}
            If ANOVA does not find significance for a category, it returns an empty dictionary for that category.
    """
    teacher_col = [col for col in df.columns if "Teacher" in col][0]
    attendance_col = [col for col in df.columns if "Attendance" in col][0]
    marks_col = [col for col in df.columns if "Marks" in col][0]

    results = {"Marks": {}, "Attendance": {}}

    # Process Attendance Scores
    attendance_df = df[[teacher_col, attendance_col]].dropna()
    attendance_counts = attendance_df[teacher_col].value_counts()
    attendance_df = attendance_df[attendance_df[teacher_col].isin(attendance_counts[attendance_counts >= 3].index)]

    if anova_significance(attendance_df):
        mean_scores = calculate_teacher_mean(attendance_df)
        iqr_scores = calculate_teacher_iqr(attendance_df)
        results["Attendance"] = calculate_weighted_score(mean_scores, iqr_scores)

    # Process Marks Scores
    marks_df = df[[teacher_col, marks_col]].dropna()
    marks_counts = marks_df[teacher_col].value_counts()
    marks_df = marks_df[marks_df[teacher_col].isin(marks_counts[marks_counts >= 3].index)]

    if anova_significance(marks_df):
        mean_scores = calculate_teacher_mean(marks_df)
        iqr_scores = calculate_teacher_iqr(marks_df)
        results["Marks"] = calculate_weighted_score(mean_scores, iqr_scores)

    return results

def calculate_weighted_score(mean_scores, iqr_scores):
    """
    Calculates the weighted score for teachers using Mean (0.6) and IQR (0.4),
    normalizing both to a 100-point scale.

    Args:
    mean_scores (dict): A dictionary with teacher names as keys and their mean values.
    iqr_scores (dict): A dictionary with teacher names as keys and their IQR values.

    Returns:
    dict: A dictionary with teacher names and their final scores.
    """
    max_mean = max(mean_scores.values(), default=1)
    max_iqr = max(iqr_scores.values(), default=1)

    teacher_scores = {}
    for teacher in mean_scores.keys():
        normalized_mean = (mean_scores[teacher] / max_mean) * 100
        normalized_iqr = (iqr_scores[teacher] / max_iqr) * 100
        teacher_scores[teacher] = round((0.6 * normalized_mean) + (0.4 * normalized_iqr), 2)

    return teacher_scores

def generate_boxplot(df, category_col, value_col, title):
    """
    Generates a box plot using Plotly to visualize the distribution of a numeric column across teachers.

    Args:
    df (pd.DataFrame): DataFrame containing the category and numeric column.
    category_col (str): Column name representing categories (e.g., "Teacher").
    value_col (str): Column name representing numerical values (e.g., "Attendance" or "Marks").
    title (str): Title for the plot.

    Returns:
    plotly.graph_objects.Figure: A Plotly figure object representing the box plot.
    """
    fig = px.box(df, x=category_col, y=value_col, title=title, points="all")
    return fig 

def plot_teacher_distributions(df):
    """
    Generates and returns two box plots to visualize the distribution of Attendance and Marks across Teachers.

    Args:
    df (pd.DataFrame): DataFrame containing columns "Teacher", "Attendance", and "Marks".

    Returns:
    tuple: (attendance_fig, marks_fig) - Two Plotly figure objects representing the box plots.
    """
    attendance_fig = generate_boxplot(df, "Teacher", "Attendance", "Distribution of Attendance by Teacher")
    marks_fig = generate_boxplot(df, "Teacher", "Marks", "Distribution of Marks by Teacher")

    return attendance_fig, marks_fig

if __name__ == "__main__":
    # Sample test DataFrame for effectiveness analysis
    data = {
        "Math Teacher": ["Mr. A", "Mr. A", "Mr. A", "Mr. B", "Mr. B", "Mr. B", "Mr. A", "Mr. A", "Mr. B", "Mr. B"],
        "Attendance": [90, 90, 78, 22, 38, 24, 75, 80, 27, 39],
        "Marks": [75, 80, 72, 0, 8, 5, 60, 65, 3, 7],
    }

    df = pd.DataFrame(data)

    # Run the analysis (assuming analyze_teacher_effectiveness exists)
    result = analyze_teacher_effectiveness(df)

    # Print results
    print("Teacher Effectiveness Scores:")
    print(result)

    # Sample dataset for box plot visualization
    data = {
        "Teacher": ["Mr. A", "Mr. A", "Mr. A", "Mr. B", "Mr. B", "Mr. B", "Mr. C", "Mr. C", "Mr. C", "Mr. C"],
        "Attendance": [90, 85, 78, 88, 92, 76, 80, 79, 95, 87],
        "Marks": [75, 80, 72, 90, 88, 85, 60, 65, 63, 70],
    }

    df = pd.DataFrame(data)

    # Call the function and get the plots
    attendance_fig, marks_fig = plot_teacher_distributions(df)

    # Display plots in Streamlit
    attendance_fig.show()
    marks_fig.show()