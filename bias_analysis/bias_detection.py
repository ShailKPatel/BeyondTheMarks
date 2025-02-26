import pandas as pd
import shap
import statsmodels.api as sm
import plotly.graph_objects as go
from sklearn.preprocessing import OneHotEncoder

def detect_bias(df: pd.DataFrame):
    """
    Detects potential gender or religious bias in student marks using multiple linear regression and SHAP analysis.

    ---
    **Mathematical Model:**
    
    The regression equation used in this analysis follows:

        Marks = β₀ + β₁ * Attendance + β₂ * Teacher_Avg + β₃ * Categorical_Factor + ε

    Where:
    - β₀: Intercept (baseline marks)
    - β₁: Impact of attendance on marks
    - β₂: Impact of teacher's average student performance
    - β₃: Influence of categorical factors (Gender or Religion)
    - ε: Random error term

    ---
    **Process Overview:**
    1. **Detect Required Columns** → Identify Attendance, Marks, Teacher, and a categorical factor (Gender or Religion).
    2. **Data Filtering** → If the teacher column exists, exclude teachers with ≤5 students. If absent, consider all students.
    3. **Replace Teacher Name with Their Average Student Marks** (or Overall Avg if no teacher column).
    4. **One-Hot Encode the Categorical Factor** without dropping the first category to retain visibility.
    5. **Perform Regression Analysis using OLS (Ordinary Least Squares)** to determine bias impact.
    6. **Use SHAP (SHapley Additive exPlanations)** to analyze feature importance.
    7. **Generate a Plotly Bar Chart with Bias Interpretation**.

    ---
    **Threshold for Bias Significance (SHAP Values Interpretation):**
    - **0 - 0.05** → Negligible Bias (Random Variance) 🟢
    - **0.05 - 0.15** → Mild Bias 🟡 (Possible but weak influence)
    - **0.15 - 0.30** → Moderate Bias 🟠 (Further investigation needed)
    - **> 0.30** → **Severe Bias** 🔴 (Strong evidence of discrimination)

    ---
    **Parameters:**
    - `df` (pd.DataFrame): DataFrame with the following structure:
        - '[Subject] Attendance': Numeric (e.g., 'Math Attendance')
        - '[Subject] Marks': Numeric (e.g., 'Math Marks')
        - '[Subject] Teacher' (Optional): Categorical (e.g., 'Math Teacher')
        - 'Gender' or 'Religion': Categorical (≤4 unique values)

    ---
    **Returns:**
    - A **Plotly bar chart (not displayed)** showing SHAP values for bias detection.
    """

    # Step 1: Detect column names dynamically
    attendance_col = next((col for col in df.columns if "Attendance" in col), None)
    marks_col = next((col for col in df.columns if "Marks" in col), None)
    teacher_col = next((col for col in df.columns if "Teacher" in col), None)

    if not attendance_col or not marks_col:
        raise ValueError("DataFrame must contain '[Subject] Attendance' and '[Subject] Marks' columns.")

    # Step 2: Identify the categorical column (Gender or Religion)
    category_col = None
    for col in df.columns:
        if col not in [attendance_col, marks_col, teacher_col] and df[col].nunique() <= 4:
            category_col = col
            break  # Stop at first valid categorical column

    if category_col is None:
        raise ValueError("DataFrame must have either a 'Gender' or 'Religion' column with at most 4 unique values.")
    
    if df[category_col].nunique() > 4:
        raise ValueError(f"Column '{category_col}' has more than 4 unique values, which is not supported.")

    # Step 3: Handle Teacher column (Replace with average marks)
    if teacher_col:
        teacher_counts = df[teacher_col].value_counts()
        df = df[df[teacher_col].isin(teacher_counts[teacher_counts > 5].index)]
        teacher_avg = df.groupby(teacher_col)[marks_col].mean()  # Compute teacher's average student marks
        df["Teacher"] = df[teacher_col].map(teacher_avg)  # Replace teacher name with average marks
        df.drop(columns=[teacher_col], inplace=True)  # Remove the original teacher column
    else:
        if len(df) <= 5:
            raise ValueError("Dataset must have more than 5 students.")
        df["Teacher"] = df[marks_col].mean()  # Assign overall average marks

    # Step 4: One-Hot Encode the categorical column (Gender or Religion)
    encoder = OneHotEncoder(sparse_output=False)  # Do NOT drop first category
    encoded_vals = encoder.fit_transform(df[[category_col]])  # Convert categorical column to numerical
    encoded_cols = encoder.get_feature_names_out([category_col])  # Get new column names for encoded values

    # Step 5: Add One-Hot Encoded columns back to DataFrame
    df_encoded = pd.DataFrame(encoded_vals, columns=encoded_cols, index=df.index)
    df = pd.concat([df, df_encoded], axis=1).drop(columns=[category_col])

    # Step 6: Define independent (X) and dependent (y) variables for regression
    X = df.drop(columns=[marks_col])  # Independent variables (attendance, teacher avg, encoded category)
    X = sm.add_constant(X)  # Add constant term for regression
    y = df[marks_col]  # Dependent variable (marks)

    # Step 7: Perform Regression Analysis (OLS Model)
    model = sm.OLS(y, X).fit()

    # Step 8: SHAP Analysis
    explainer = shap.Explainer(model.predict, X)
    shap_values = explainer(X)

    # Step 9: Compute Mean Absolute SHAP Values (Bias Impact)
    mean_shap_values = shap_values.values.mean(axis=0)  # it's a NumPy array
    shap_value_dict = dict(zip(X.columns, mean_shap_values.tolist()))
    print(shap_value_dict)

    # Step 10: Separate Positive and Negative SHAP Values
    positive_shap = {}
    negative_shap = {}

    for feature, value in shap_value_dict.items():
        if value >= 0:
            positive_shap[feature] = value
        else:
            negative_shap[feature] = value
    
    # Step 11: Create Stacked Bar Chart with Positive (Blue) and Negative (Red) Biases
    positive_features = list(positive_shap.keys())
    positive_values = list(positive_shap.values())

    negative_features = list(negative_shap.keys())
    negative_values = list(negative_shap.values())
    
    fig = go.Figure()

    # Positive bars
    fig.add_trace(go.Bar(
        x=positive_features,
        y=positive_values,
        name='Positive Shap Values',
        marker_color='#636EFA'
    ))

    # Negative bars
    fig.add_trace(go.Bar(
        x=negative_features,
        y=negative_values,
        name='Negative Shap Values',
        marker_color='#EF553B'
    ))

    fig.update_layout(
        title='Shapley Value Analysis',
        xaxis_title='Features',
        yaxis_title='Shapley Values',
        barmode='relative' # very important for clarity.
    )
    
    fig.add_annotation(
        x=0.5, y=max(abs(mean_shap_values)) * 1.1, text="Bias > 0.15 is considered significant. Bias > 0.30 is severe.",
        showarrow=False, font=dict(size=12, color="red"), xref="paper", yref="y"
    )

    return fig  # Return the Plotly figure object


# Example usage
if __name__ == "__main__":
    # Sample Data

    data = { 
        "Math Teacher": ["A", "A", "A", "B", "B", "B", "A", "A", "A", "B", "B", "B"],
        "Gender": ["Male", "Female", "Trans", "Male", "Female", "Trans", "Male", "Female", "Trans", "Male", "Female", "Trans"],
        "Math Attendance": [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
        "Math Marks": [85, 88, 6, 78, 85, 5, 80, 90, 5, 88, 86, 5],  # Trans students have much lower marks
    }

    df = pd.DataFrame(data)

    # Run Bias Analysis
    bias_graph = detect_bias(df)
    bias_graph.show()  # Display the returned Plotly figure
