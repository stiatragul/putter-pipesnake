import pandas as pd
import sys

def print_unique_values(csv_file, column_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Extract unique values from the specified column
    unique_values = df[column_name].unique()

    # Print the unique values
    print(f"Unique values in column '{column_name}':")
    for value in unique_values:
        print(value)

if __name__ == "__main__":
    # Check if correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file> <column_name>")
        sys.exit(1)

    # Get CSV file path and column name from command-line arguments
    csv_file = sys.argv[1]
    column_name = sys.argv[2]

    # Call the function to print unique values in the specified column
    print_unique_values(csv_file, column_name)
