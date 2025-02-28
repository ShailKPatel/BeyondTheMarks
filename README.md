# Installation Guide for BeyondTheMarks

## Prerequisites
Before you begin, ensure you have the following installed:
- **Python** (Latest stable version recommended)
- **pip** (Python package manager)

## Installation Steps

1. **Clone the Repository**  
   If you haven't already, clone the BeyondTheMarks repository:
   ```sh
   git clone https://github.com/ShailKPatel/BeyondTheMarks
   cd BeyondTheMarks
   ```

2. **Install Dependencies**  
   Run the following command to install all required dependencies from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application**  
   Use the command below to start the application with Streamlit:
   ```sh
   streamlit run main.py
   ```

## Project Structure
The project is organized as follows:
```
BeyondTheMarks
│   LICENSE
│   main.py
│   README.md
│   requirements.txt
│
├───.streamlit
│       config.toml
│
├───analysis
│       subject_analysis.py
│       teacher_analysis.py
│
├───bias_analysis
│       bias_detection.py
│
├───core_functionality
│       data_validator.py
│
├───images
│       logo.png
│
├───reviews
│       recent_reviews.txt
│       word_count.txt
│
├───samplefiles
│       test1.csv
│       test2.csv
│       test3.csv
│       test4.csv
│
└───views
        Data_Dissector.py
        Home.py
        Reviews.py
        Tech_Wizardry.py
        The_Brains_Behind.py
```

# Documentation for main.py

## Overview
The `main.py` script sets up a **multi-page Streamlit application** with a structured navigation system. It provides an interface for users to navigate between different sections of the app, each serving a distinct purpose.

## Features
- **Multi-Page Navigation**: Allows seamless switching between different pages.
- **Categorized Sections**:
  1. **Home**: Introduction and overview of the project.
  2. **Data Dissector**: Provides core analysis functionalities.
  3. **The Brains Behind**: Displays credits for contributors.
  4. **Tech Wizardry**: Showcases the technologies used in the project.
  5. **Reviews**: Displays user feedback and reviews.

## File Navigation Setup
The script defines five pages, each corresponding to a separate Python file located in the `views` directory:
```python
home = st.Page("views/Home.py", icon='🏠')
data_dissector = st.Page("views/Data_Dissector.py", icon='🔬')
the_brains_behind = st.Page("views/The_Brains_Behind.py", icon='🧠')
tech_wizardry = st.Page("views/Tech_Wizardry.py", icon='🛠️')
reviews = st.Page("views/Reviews.py", icon='📨')
```
Each page file should contain its own Streamlit logic and UI components.

## Navigation System
The script uses `st.navigation()` to create a structured menu:
```python
pg = st.navigation([
    home,
    data_dissector,
    the_brains_behind,
    tech_wizardry,
    reviews
])
```
This ensures a well-organized navigation bar, allowing users to switch between sections effortlessly.

## Notes
- Each page file (`Home.py`, `Data_Dissector.py`, etc.) must be properly configured with Streamlit components.
- Ensure that all necessary dependencies are installed to avoid runtime errors.

## Conclusion
This `main.py` script serves as the entry point for the **BeyondTheMarks** Streamlit application, providing a structured and user-friendly interface for data analysis, reviews, and project insights.

# Documentation for Views

## Overview
The `views` directory contains individual Python scripts responsible for rendering different sections of the **Beyond The Marks** Streamlit application. Each script defines the layout and functionality of a specific page within the app.

---

## Home.py
### Purpose
The `Home.py` script serves as the landing page of the application, introducing users to **Beyond The Marks** and providing navigation to key sections.

### Features
- Displays the project logo.
- Provides a **brief description** of the project and its functionalities.
- Lists key features such as **file validation, teacher analysis, and bias detection**.
- Offers quick navigation links to other views (`Data Dissector`, `The Brains Behind`, `Tech Wizardry`, and `Reviews`).
- Shows footer information including licensing details.

### Key Components
- **Project Overview**: Explains the purpose and scope of the project.
- **Key Features**: Highlights core functionalities.
- **Navigation Links**: Directs users to different sections of the application.
- **Footer**: Displays license and developer information.

---

## Tech_Wizardry.py
### Purpose
The `Tech_Wizardry.py` script provides an **insight into the technologies** used to build the application.

### Features
- Displays the project logo.
- Lists the **core technology stack**, including Python, Streamlit, and key data science libraries.
- Explains **mathematical techniques** like ANOVA and One-Hot Encoding used in bias detection.
- Provides a lighthearted overview of **why the technology stack was chosen**.

### Key Components
- **Core Tech Stack**: Describes programming languages, frameworks, and libraries used.
- **Mathematical Wizardry**: Explains the statistical techniques powering analysis.
- **Why This Works**: A fun and engaging explanation of the tool’s effectiveness.
- **Fun Fact**: Adds a humorous touch to the documentation.

---

## The_Brains_Behind.py
### Purpose
The `The_Brains_Behind.py` script gives credit to the **contributors** behind the project.

### Features
- Displays the project logo.
- Highlights **Shail K Patel** as the lead developer.
- Provides links to **LinkedIn and GitHub** profiles.
- Includes a fun fact about the project's development journey.

### Key Components
- **Contributor Information**: Acknowledges key developers.
- **Social Links**: Provides ways to connect with the contributors.
- **Fun Fact**: Adds personality to the documentation.

---

# Documentation for Review.py

## Overview
The `Review.py` script is a **Streamlit-based feedback module** for the **BeyondTheMarks** project. It allows users to submit and view reviews, analyzes word frequencies, and maintains a record of recent feedback.

## Features
- **Review Submission & Display**: Users can submit feedback, which is displayed dynamically.
- **Queue System**: Stores up to six recent reviews using a queue.
- **Word Frequency Analysis**: Tracks the most frequently used words in reviews.
- **Persistent Storage**:
  - Reviews are stored in `reviews/recent_reviews.txt`.
  - Word counts are stored in `reviews/word_count.txt`.
- **Graphical Representation**: Displays the top 10 most common words using a **Plotly** bar chart.

## Queue System
The script defines a `QueueWithReverse` class for managing a **fixed-size queue** (max 6 entries):
```python
class QueueWithReverse:
    THRESHOLD = 6
    ...
```
- **enqueue(entry)**: Adds an entry; removes the oldest if full.
- **dequeue()**: Removes and returns the oldest entry.
- **retrieve()**: Returns all stored entries.

## Persistent Review Storage
Reviews are saved and loaded via:
```python
def extract_reviews():
def preserve_reviews(repository):
```
- `extract_reviews()`: Reads stored reviews from `recent_reviews.txt`.
- `preserve_reviews(repository)`: Saves queue data back to the file.

## Word Frequency Tracker
A custom hash map (`CustomHashMap`) tracks word frequencies:
```python
class CustomHashMap:
    def add(word):
    def get_items():
    def load_word_count():
    def save_word_count():
```
- **add(word)**: Increments the count of a word.
- **get_items()**: Returns the **top 10 most frequent words**.
- **load_word_count()**: Reads data from `word_count.txt`.
- **save_word_count()**: Writes word frequencies to `word_count.txt`.

## Streamlit UI Components
### 1️⃣ **Displaying Recent Reviews**
- Shows up to **6 recent reviews** in a **grid layout**:
```python
reviews = review_queue.retrieve()
columns = st.columns(min(3, total_entries - i))
```

### 2️⃣ **Top 10 Word Frequency Analysis**
- **Displays a Plotly bar chart** of the most used words:
```python
fig = go.Figure(data=[go.Bar(x=words, y=frequencies, marker_color='indianred')])
st.plotly_chart(fig)
```

### 3️⃣ **Submitting a Review**
- Users enter text in a **text area** and submit:
```python
user_review = st.text_area("Got Complaint.. Er... Suggestion? Drop them here", "")
```
- The review is added to the queue and stored persistently.
- **Balloon animation** appears on submission.

## Notes
- The **review queue is limited to six entries**.
- **Words are case-insensitive** in frequency tracking.
- **Data persistence ensures reviews and word counts remain after a restart.**

# Data Validator Module

## Overview
The `data_validator.py` module provides functionality for validating and processing CSV and Excel files containing student data. It ensures that the data is correctly structured, contains necessary columns, and adheres to specific rules such as numeric constraints and unique identifiers.

## Features
- Supports `.csv`, `.xlsx` file formats.
- Validates file integrity and structure.
- Dynamically detects subjects based on column naming conventions.
- Ensures `Roll No` uniqueness and numeric constraints for marks and attendance.
- Raises custom exceptions for various validation failures.

## Custom Exceptions
### `InvalidExtensionError`
Raised when the file format is unsupported.

### `CorruptedFileError`
Raised when the file cannot be read, possibly due to corruption.

### `InvalidDataStructureError`
Raised when the file lacks necessary columns or has an incorrect structure.

### `UnknownColumnError`
Raised when an unexpected column is found in the dataset.

## Functions

### `validate_and_convert_file(file)`
**Description:**
Validates the structure and content of a given file and converts it into a Pandas DataFrame.

**Parameters:**
- `file`: The uploaded file object.

**Returns:**
- `tuple`: `(Pandas DataFrame, NumPy array of detected subjects)`

**Validation Steps:**
1. Check file extension.
2. Load data into a Pandas DataFrame.
3. Verify required columns (`Roll No`, subject-wise `Marks` and `Attendance`).
4. Ensure subject-based column relationships (e.g., `Math Marks` must have `Math Attendance`).
5. Detect unknown columns and raise an error if found.
6. Ensure at least one subject exists.
7. Convert detected subjects into a NumPy array.
8. Call `validate_data(df)` for further validation.

### `validate_data(df)`
**Description:**
Validates the contents of the Pandas DataFrame by ensuring uniqueness, numeric constraints, and value ranges.

**Parameters:**
- `df`: A Pandas DataFrame containing the dataset.

**Returns:**
- `Pandas DataFrame`: The validated and cleaned dataset.

**Validation Steps:**
1. Ensure `Roll No` values are unique.
2. Identify all `Marks` and `Attendance` columns dynamically.
3. Ensure these columns are numeric.
4. Check if values are within the valid range (0-100).
5. Round values to two decimal places.

# Teacher Effectiveness Analysis using ANOVA

## Overview
This Python script analyzes the effectiveness of teachers by examining the variance in student performance metrics such as attendance and marks. It applies statistical methods like one-way ANOVA and calculates weighted scores based on mean and interquartile range (IQR) values.

## Features
- **ANOVA Test**: Determines if there is a significant difference in marks or attendance across different teachers.
- **Mean and IQR Calculation**: Computes the average and interquartile range for each teacher.
- **Weighted Score Computation**: Uses a 60-40 weighted formula to rank teachers based on their effectiveness.
- **Box Plot Visualization**: Generates distribution plots for attendance and marks across teachers.

## Functions
### 1. `anova_significance(df)`
**Purpose:**
- Performs a one-way ANOVA test to check if there is a significant difference in marks or attendance across different teachers.

**Parameters:**
- `df` (DataFrame): A DataFrame with two columns:
  - One column for teachers (e.g., "Math Teacher").
  - One numeric column ("Marks" or "Attendance").

**Returns:**
- `True` if the ANOVA test finds a significant difference (`p-value < 0.1`), otherwise `False`.

---
### 2. `calculate_teacher_mean(df)`
**Purpose:**
- Computes the mean of the numeric column (Marks or Attendance) for each teacher.

**Returns:**
- A dictionary `{teacher_name: mean_value}`.

---
### 3. `calculate_teacher_iqr(df)`
**Purpose:**
- Computes the interquartile range (IQR) of the numeric column (Marks or Attendance) for each teacher.

**Returns:**
- A dictionary `{teacher_name: iqr_value}`.

---
### 4. `analyze_teacher_effectiveness(df)`
**Purpose:**
- Determines teacher effectiveness based on ANOVA significance tests for marks and attendance.
- Calculates mean, IQR, and weighted scores for teachers if significant differences exist.

**Returns:**
- A dictionary:
  ```
  {
    "Marks": {teacher_name: weighted_score},
    "Attendance": {teacher_name: weighted_score}
  }
  ```

---
### 5. `calculate_weighted_score(mean_scores, iqr_scores)`
**Purpose:**
- Computes a weighted score for each teacher using a 60-40 formula:
  - **60% weight for Mean**
  - **40% weight for IQR**

**Returns:**
- A dictionary `{teacher_name: weighted_score}`.

---
### 6. `generate_boxplot(df, category_col, value_col, title)`
**Purpose:**
- Generates a box plot to visualize the distribution of attendance or marks for each teacher.

**Returns:**
- A Plotly figure object.

---
### 7. `plot_teacher_distributions(df)`
**Purpose:**
- Generates box plots for attendance and marks distributions across teachers.

**Returns:**
- Two Plotly figure objects: one for attendance and one for marks.

## Usage Example
```python
import pandas as pd

data = {
    "Teacher": ["A", "A", "B", "B", "C", "C", "A", "B", "C"],
    "Marks": [80, 85, 78, 82, 88, 90, 83, 79, 87],
    "Attendance": [90, 95, 85, 80, 88, 92, 93, 81, 89]
}
df = pd.DataFrame(data)

results = analyze_teacher_effectiveness(df)
print(results)
```



## Notes
- Teachers with fewer than 3 data points are excluded from the analysis.
- ANOVA test significance is set at `p-value < 0.1` to detect meaningful variations.

This script helps in evaluating the impact of teachers based on student attendance and marks using statistical analysis and visualization tools.

# Subject Performance Analysis Documentation

## Function: `analyze_subject_performance`

### Description
This function analyzes student performance across multiple subjects based on marks and attendance. It generates visualizations to explore correlations, distribution of marks, and the relationship between attendance and marks.

### Parameters
- `df (pd.DataFrame)`: A dataset containing student performance details.
- `subject_names (list)`: A list of subjects to analyze (e.g., `["Math", "Science", "English"]`).

### Returns
A tuple containing:
1. **Correlation Matrix Heatmap** (Plotly figure) - Displays correlations between subject marks if multiple subjects are present.
2. **Box Plot of Subject Marks** (Plotly figure) - Shows the distribution of marks for each subject if multiple subjects are present.
3. **Scatter Plots (List of Plotly figures)** - Each plot illustrates the relationship between attendance and marks for a subject, including a regression line.

### Workflow
1. **Correlation Matrix**
   - Extracts subject marks columns and computes a correlation matrix.
   - Generates a heatmap to visualize correlations (if multiple subjects are present).

2. **Box Plot of Marks Distribution**
   - Converts marks data to a long format for visualization.
   - Creates a box plot showing the spread of marks across subjects.

3. **Scatter Plots for Attendance vs. Marks**
   - Iterates through each subject.
   - Fits a simple linear regression model using attendance as the independent variable and marks as the dependent variable.
   - Displays the regression equation on each scatter plot.

### Example Usage
```python
import pandas as pd

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
subjects = ["Math", "Science", "English"]
fig1, fig2, scatter_list = analyze_subject_performance(df, subjects)

if fig1: fig1.show()
if fig2: fig2.show()
for fig in scatter_list:
    fig.show()
```

### Edge Cases Considered
- If only one subject is provided, correlation matrix and box plot are not generated.
- Handles different subject names dynamically.
- Accounts for missing values by converting data types before regression.

### Notes
- Regression analysis is used to determine the effect of attendance on marks.
- Scatter plots include trend lines for better interpretation of relationships.

# BeyondTheMarks - Bias Detection Documentation

## Overview
The `detect_bias` function analyzes potential bias in student marks based on gender or religion using multiple linear regression and SHAP analysis. It helps identify whether a categorical factor influences student grades disproportionately.

---
## Mathematical Model

The regression equation used in this analysis follows:

\[ \text{Marks} = \beta_0 + \beta_1 \times \text{Attendance} + \beta_2 \times \text{Teacher\_Avg} + \beta_3 \times \text{Categorical\_Factor} + \varepsilon \]

Where:
- **\( \beta_0 \)**: Intercept (baseline marks)
- **\( \beta_1 \)**: Impact of attendance on marks
- **\( \beta_2 \)**: Impact of teacher's average student performance
- **\( \beta_3 \)**: Influence of categorical factors (Gender or Religion)
- **\( \varepsilon \)**: Random error term

---
## Process Overview

1. **Detect Required Columns** → Identify `Attendance`, `Marks`, `Teacher`, and a categorical factor (Gender or Religion).
2. **Data Filtering** → If the teacher column exists, exclude teachers with ≤5 students. If absent, consider all students.
3. **Replace Teacher Name with Their Average Student Marks** (or Overall Avg if no teacher column).
4. **One-Hot Encode the Categorical Factor** without dropping the first category to retain visibility.
5. **Perform Regression Analysis using OLS (Ordinary Least Squares)** to determine bias impact.
6. **Use SHAP (SHapley Additive exPlanations)** to analyze feature importance.
7. **Generate a Plotly Bar Chart with Bias Interpretation**.

---
## Bias Significance Threshold (SHAP Value Interpretation)
- **0 - 0.05** → Negligible Bias 🟢
- **0.05 - 0.15** → Mild Bias 🟡 (Possible but weak influence)
- **0.15 - 0.30** → Moderate Bias 🟠 (Further investigation needed)
- **> 0.30** → **Severe Bias** 🔴 (Strong evidence of discrimination)

---
## Parameters
- `df` (`pd.DataFrame`): DataFrame with the following structure:
  - `"[Subject] Attendance"`: Numeric (e.g., `"Math Attendance"`)
  - `"[Subject] Marks"`: Numeric (e.g., `"Math Marks"`)
  - `"[Subject] Teacher"` (Optional): Categorical (e.g., `"Math Teacher"`)
  - `"Gender"` or `"Religion"`: Categorical (≤4 unique values)

---
## Returns
- A **Plotly bar chart** showing SHAP values for bias detection (not displayed directly in function).

---
## Implementation Details

### Step 1: Identify Required Columns
- Detect attendance, marks, and teacher columns dynamically.
- Ensure at least one categorical column (Gender or Religion) exists with ≤4 unique values.

### Step 2: Handle Teacher Column
- If `Teacher` exists, replace it with their average student marks.
- If no `Teacher` column, use the overall class average.

### Step 3: Encode Categorical Column
- Apply **One-Hot Encoding** without dropping any category to retain full visibility.

### Step 4: Regression Analysis
- Define **independent variables (X)**: Attendance, Teacher Avg, Encoded Categorical Values.
- Define **dependent variable (y)**: Marks.
- Perform **Ordinary Least Squares (OLS) Regression**.

### Step 5: SHAP Analysis
- Compute SHAP values to determine each feature’s contribution.
- Categorize SHAP values as positive (blue) or negative (red) for visual interpretation.

### Step 6: Generate Plotly Visualization
- Display a **stacked bar chart** showing bias influence based on SHAP values.
- Highlight severity thresholds for interpretation.

---
## Example Usage

```python
import pandas as pd

data = {
    "Math Teacher": ["A", "A", "A", "B", "B", "B", "A", "A", "A", "B", "B", "B"],
    "Gender": ["Male", "Female", "Trans", "Male", "Female", "Trans", "Male", "Female", "Trans", "Male", "Female", "Trans"],
    "Math Attendance": [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
    "Math Marks": [85, 88, 6, 78, 85, 5, 80, 90, 5, 88, 86, 5],
}

df = pd.DataFrame(data)

bias_graph = detect_bias(df)
bias_graph.show()
```

---
## Notes
- The function assumes that gender or religion is the primary categorical factor influencing bias detection.
- Teachers with ≤5 students are excluded to ensure statistical validity.
- The function **does not** infer causation but highlights statistical correlations.

---
# BeyondTheMarks Documentation

## Introduction
BeyondTheMarks is an analytical tool designed to process and evaluate student performance data from academic marksheets. The application identifies trends, biases, and effectiveness in teaching methodologies, providing deep insights into the educational environment. With features like professor performance analysis, bias detection, and subject performance comparison, it transforms raw data into actionable insights.

## Features

### 1. **Data Upload & Validation**
- Supports `.csv` and `.xlsx` formats.
- Performs rigorous validation to ensure data integrity.
- Enforces structural laws:
  - Unique Roll Numbers.
  - Proper subject-wise attendance and marks format.
  - Optional but structured teacher column.
  - Numerical values within permissible limits.

### 2. **Professor Performance Analysis**
- Identifies subject-wise teacher effectiveness.
- Uses attendance and marks to compute a teacher score.
- Visualizes teacher performance through interactive graphs.
- Generates a structured performance matrix for better comparison.

### 3. **Bias Detection**
#### **Gender Bias Analysis**
- Detects gender-based discrepancies in marks and attendance.
- Uses visualization techniques to highlight potential bias.
- Requires a `Gender` column for analysis.

#### **Religious Bias Analysis**
- Identifies patterns of religious bias in academic performance.
- Relies on a `Religion` column for meaningful insights.
- Visual representations make bias detection intuitive.

### 4. **Subject Performance Analysis**
- Compares subjects based on overall performance.
- Displays statistical insights using:
  - Correlation matrix
  - Box plots
  - Scatter plots
- Helps in understanding subject difficulty levels.

## Usage

### **Step 1: Upload Data**
1. Click the "Upload" button and select a valid `.csv` or `.xlsx` file.
2. The system automatically validates the data and provides feedback.
3. If successful, the data appears for further analysis.

### **Step 2: Choose an Analysis Mode**
- **Professor Performance Analysis**: Evaluates teacher effectiveness.
- **Gender Bias Detection**: Detects biases based on gender.
- **Religious Bias Detection**: Identifies biases related to religion.
- **Subject Performance Comparison**: Analyzes subject difficulty and trends.

### **Step 3: Visual Interpretation**
- Graphs and matrices provide deep insights.
- Any detected biases or anomalies are highlighted.
- The final data visualization helps in decision-making.

## Error Handling
- If invalid data is uploaded, clear error messages guide correction.
- Users must ensure compliance with the "Grand Data Upload Rulebook."
