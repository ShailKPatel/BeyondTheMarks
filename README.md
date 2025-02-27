---

# **Learning Impact Analysis Tool** 📊🎓  
_A smart data-driven tool to analyze student performance and detect potential biases._  

## **Overview**  
The Learning Impact Analysis Tool processes academic records, evaluates teacher effectiveness, and checks for potential biases (gender, religion). It also provides individual student performance insights and visualizations.  

### **Key Features**  
✔ **File Validation & Parsing**: Accepts CSV & Excel files, ensuring correct format.  
✔ **Teacher Efficiency Analysis**: Uses **ANOVA** to measure a teacher's impact.  
✔ **Bias Detection**: Analyzes **gender** and **religion-based** performance trends.  
✔ **Student Search & Comparison**: Allows percentile-based performance checks.  
✔ **3D Data Visualization**: Plots **attendance vs. theory vs. practical marks**.  
✔ **Error Handling**: Custom exceptions for invalid files, missing data, and format issues.  

---

## **Installation & Setup** 🛠️  
### **Prerequisites**  
Ensure you have **Python 3.x** installed along with the following dependencies:  
```bash
pip install pandas numpy plotly scipy openpyxl
```

---

## **How to Use** 🚀  
### **1️⃣ Upload & Validate File**  
Your dataset must be in **CSV or Excel format** (`.csv`, `.xls`, `.xlsx`, etc.).  
It should contain at least:
- **Roll No** (Mandatory)
- **At least one subject with "Marks" and "Attendance"**  
- **Optional columns**: Name, Gender, Religion, Teacher  

🔹 **Example Format:**  
```csv
Roll No, Name, Gender, Religion, Maths Marks, Maths Attendance, Maths Teacher, Science Marks, Science Attendance, Science Teacher
101, Alice, Female, Hindu, 95.5, 88.2, Mr. Sharma, 85, 78, Ms. Verma
```
🔹 **Uploading the file:**
```python
df, subjects = validate_and_convert_file("test_data.csv")
```

---

### **2️⃣ Data Processing & Analysis**  
#### ✅ **Teacher Efficiency Analysis**  
Compares each teacher’s students against the general student population. Uses **ANOVA** to measure significance.  
```python
analyze_teacher_effectiveness(df)
```

#### ✅ **Gender & Religion Bias Detection**  
Detects statistical disparities in performance.  
```python
check_gender_bias(df)
check_religion_bias(df)
```

#### ✅ **Student Performance Lookup**  
Allows searching by **Roll No or Name** and provides percentile-based comparison.  
```python
lookup_student_performance(df, "Alice")
```

---

### **3️⃣ Visualization** 🎨  
#### 📊 **Histogram of Student Marks**  
```python
plot_student_histogram(df, "Maths Marks")
```

#### 📈 **3D Scatter Plot (Attendance vs. Theory vs. Practical)**  
```python
plot_3d_attendance_vs_marks(df)
```

---

## **Error Handling** 🚨  
Custom exceptions ensure smooth execution.  
| Exception | Cause |
|-----------|-------------|
| `InvalidExtensionError` | File type not CSV or Excel |
| `CorruptedFileError` | File cannot be opened |
| `InvalidDataStructureError` | Missing required columns |
| `UnknownColumnError` | Extra columns not allowed |
| `ValueError` | Non-numeric marks/attendance or out-of-range values |

---

## **Contributing** 🤝  
1. **Fork** the repo  
2. **Create a feature branch**  
3. **Submit a PR with clear documentation**  

---

## **Future Enhancements** 🔮  
- 📊 **More advanced ML models** for student performance prediction.  
- 📌 **Dashboard UI** for easier interaction.  
- 📅 **Multi-year data support** for trends over time.  

---

## **License** 📜  
This project is licensed under the **MIT License**.  