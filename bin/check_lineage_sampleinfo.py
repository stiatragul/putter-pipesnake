
# Finds duplicate rows in lineage column of sample info file.

import pandas as pd
import sys

def find_issues_in_column(csv_file, column_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Find duplicate values in the specified column
    duplicate_rows = df[df.duplicated(subset=[column_name], keep=False)]

    # Find rows with issues in the specified column
    issue_rows = df[df[column_name].str.contains(r'[()\\\/ ]', na=False)]

    if duplicate_rows.empty:
        print(f"No duplicate values found in column '{column_name}'.")
    else:
        print(f"Duplicates found in column '{column_name}':")
        print(duplicate_rows)

    if issue_rows.empty:
        print(f"No issues found in column '{column_name}'.")
    else:
        print(f"Issues found in column '{column_name}':")
        print(issue_rows)

if __name__ == "__main__":
    # Check if correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file> <column_name>")
        sys.exit(1)

    # Get CSV file path and column name from command-line arguments
    csv_file = sys.argv[1]
    column_name = sys.argv[2]

    # Call the function to find duplicates and issues in the specified column
    find_issues_in_column(csv_file, column_name)
