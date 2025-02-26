import pandas as pd
import numpy as np

class InvalidExtensionError(Exception):
    """Raised when the file extension is not supported."""
    def __init__(self, message="File must be in CSV or Excel format (.csv, .xls, .xlsx, .xlsm, .xlsb)."):
        self.message = message
        super().__init__(self.message)

class CorruptedFileError(Exception):
    """Raised when the file cannot be opened or is corrupted."""
    def __init__(self, message="The file appears to be corrupted or unreadable."):
        self.message = message
        super().__init__(self.message)

class InvalidDataStructureError(Exception):
    """Raised when the file structure does not meet the required format."""
    def __init__(self, message="The file structure is invalid. Please check missing columns."):
        self.message = message
        super().__init__(self.message)

class UnknownColumnError(Exception):
    """Raised when an unexpected column is detected in the file."""
    def __init__(self, column_name):
        self.message = f"Column '{column_name}' is not allowed."
        super().__init__(self.message)

def validate_and_convert_file(file):
    """
    Validates the uploaded file and converts it into a Pandas DataFrame.

    Steps:
    1. Check if the file has a valid extension (.csv, .xls, .xlsx, .xlsm, .xlsb).
    2. Try to load it into a DataFrame, handling potential corruption errors.
    3. Ensure the file has at least Roll No, Attendance, and Marks.
    4. Dynamically check for subject-based columns and validate their structure.
    5. Ensure there are no unexpected columns.
    6. Return the cleaned DataFrame and an array of detected subjects.

    Args:
    file (file object): The uploaded file.

    Returns:
    tuple: (Pandas DataFrame, NumPy array of detected subjects).
    """
    # Step 1: Check file extension
    valid_extensions = ('.csv', '.xls', '.xlsx', '.xlsm', '.xlsb')
    
    if not file.name.endswith(valid_extensions):
        raise InvalidExtensionError()

    try:
        # Step 2: Load the file into a DataFrame
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

    except Exception:
        raise CorruptedFileError()

    # Step 3: Define required & optional columns
    mandatory_columns = {"Roll No"}
    optional_columns = {"Name", "Gender", "Religion"}
    allowed_columns = set(mandatory_columns | optional_columns)  # Allowed basic columns

    detected_subjects = set()  # Store detected subjects dynamically

    for col in df.columns:
        # If a column is for marks, extract subject name
        if col.endswith(" Marks"):
            subject_name = col.replace(" Marks", "")
            detected_subjects.add(subject_name)
            
            # Ensure the corresponding "Attendance" column exists
            if f"{subject_name} Attendance" not in df.columns:
                raise InvalidDataStructureError(f"Missing '{subject_name} Attendance' for '{subject_name} Marks'.")

            # Add subject-related columns to allowed list
            allowed_columns.add(f"{subject_name} Marks")
            allowed_columns.add(f"{subject_name} Attendance")
            allowed_columns.add(f"{subject_name} Teacher")  # Teacher is optional

        # If column is for attendance, ensure "Marks" also exists
        elif col.endswith(" Attendance"):
            subject_name = col.replace(" Attendance", "")

            # If marks are missing for this subject, raise an error
            if f"{subject_name} Marks" not in df.columns:
                raise InvalidDataStructureError(f"Missing '{subject_name} Marks' for '{subject_name} Attendance'.")

            # Add subject-related columns to allowed list
            allowed_columns.add(f"{subject_name} Marks")
            allowed_columns.add(f"{subject_name} Attendance")
            allowed_columns.add(f"{subject_name} Teacher")  # Teacher is optional

        elif col.endswith(" Teacher"):
            subject_name = col.replace(" Teacher", "")

            # Ensure the subject has Marks & Attendance
            if f"{subject_name} Marks" not in df.columns or f"{subject_name} Attendance" not in df.columns:
                raise InvalidDataStructureError(f"'{subject_name} Teacher' column is present but '{subject_name} Marks' or '{subject_name} Attendance' is missing.")

            # Add subject-related columns to allowed list
            allowed_columns.add(f"{subject_name} Marks")
            allowed_columns.add(f"{subject_name} Attendance")
            allowed_columns.add(f"{subject_name} Teacher")

        # Step 4: Check for unknown columns
        elif col not in allowed_columns:
            raise UnknownColumnError(col)

    # Step 5: Ensure at least one subject is present
    if not detected_subjects:
        raise InvalidDataStructureError("At least one subject (with Marks and Attendance) is required.")

    # Step 6: Convert detected subjects to a NumPy array
    subject_array = np.array(list(detected_subjects))

    # Step 7: Validate Validate the DataFrame
    df = validate_data(df)

    return df, subject_array

def validate_data(df):
    """
    Validates the data inside the DataFrame.

    Checks performed:
    1. Ensures all 'Roll No' values are unique.
    2. Ensures all 'Marks' and 'Attendance' columns:
        - Are strictly numeric.
        - Have values between 0 and 100.
        - Are rounded to 2 decimal places.

    Args:
    df (Pandas DataFrame): The dataset to validate.

    Returns:
    Pandas DataFrame: The validated and updated DataFrame with rounded numeric values.

    Raises:
    ValueError: If any validation check fails.
    """
    
    # Step 1: Ensure "Roll No" is unique
    if df["Roll No"].duplicated().any():
        raise ValueError("Duplicate values found in 'Roll No'. Each student must have a unique Roll Number.")

    # Step 2: Identify all "Marks" and "Attendance" columns dynamically
    subject_columns = [col for col in df.columns if col.endswith((" Marks", " Attendance"))]

    for col in subject_columns:
        # Step 3: Ensure column is numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric.")

        # Step 4: Ensure values are within [0, 100]
        if (df[col] < 0).any() or (df[col] > 100).any():
            raise ValueError(f"Column '{col}' contains values outside the valid range (0-100).")

        # Step 5: Round values to 2 decimal places (in-place update)
        df[col] = df[col].round(2)

    return df  # Return updated DataFrame

if __name__ == "__main__":
    with open("test1.csv", "r") as file:
        df, subjects = validate_and_convert_file(file)
    print(df)
    print(subjects)

