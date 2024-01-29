import os
import csv
import shutil
import argparse

def rename_files(csv_file, input_directory):
    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    # Read the CSV file
    name_mapping = {}
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            old_name = row.get('old')
            new_name = row.get('new')
            if old_name and new_name:
                name_mapping[old_name] = new_name

    # Create a new directory for corrected files at the same level as the input directory
    output_directory = os.path.join(os.path.dirname(input_directory.rstrip('/')), f"{os.path.basename(input_directory)}_corrected")
    os.makedirs(output_directory, exist_ok=True)

    # List to keep track of changed filenames
    changed_files = []

    # Iterate over .fasta files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".fasta"):
            old_name = filename[:-6]  # Remove ".fasta" extension
            if old_name in name_mapping:
                new_name = name_mapping[old_name] + ".fasta"
                # Copy the file to the output directory with the new name
                shutil.copy2(os.path.join(input_directory, filename), os.path.join(output_directory, new_name))
                print(f"Renamed {filename} to {new_name} in {output_directory}")
                changed_files.append(f"{old_name} -> {new_name}")
            else:
                # If no mapping found, copy the file without renaming
                shutil.copy2(os.path.join(input_directory, filename), os.path.join(output_directory, filename))
                print(f"Copied {filename} to {filename} in {output_directory}")

    # Write list of changed filenames to a text file
    with open(os.path.join(output_directory, "00_changed_files.txt"), "w") as file:
        file.write("This is automatically generated to confirm that the following files have been renamed:\n\n")
        for filename in changed_files:
            file.write(filename + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename .fasta files based on a CSV mapping.")
    parser.add_argument("csv_file", help="Path to the CSV file containing old and new filenames mapping.")
    parser.add_argument("input_directory", help="Path to the input directory containing .fasta files.")
    args = parser.parse_args()

    rename_files(args.csv_file, args.input_directory)
