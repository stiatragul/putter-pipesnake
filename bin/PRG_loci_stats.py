import os
import sys
import pandas as pd
import re

# Function to count > headers in a fasta file
def count_sample_headers(file_path):
    counts = {"AHE": 0, "UCE": 0, "Gene": 0}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('>AHE'):
                counts["AHE"] += 1
            elif line.startswith('>uce'):
                counts["UCE"] += 1
            elif line.startswith('>'):
                counts["Gene"] += 1
    return counts

# Get directory path from command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <fasta_directory>")
    sys.exit(1)

fasta_directory = sys.argv[1]

# List to store counts for each file
counts_list = []

# Regular expression pattern to extract specimen ID
pattern = r'(?<=_)[A-Z_]+\S*'

# Iterate through fasta files in the directory
for filename in os.listdir(fasta_directory):
    if filename.endswith(".fasta"):  # Assuming fasta file extension is .fasta
        file_path = os.path.join(fasta_directory, filename)
        counts = count_sample_headers(file_path)
        
        # Extract specimen ID from filename
        specimen_id = re.search(pattern, filename[:-6]).group()
        # Replace underscores with spaces
        specimen_id = specimen_id.replace("_", " ")
        
        # Add columns for loci to the counts dictionary
        counts["file name"] = filename[:-6]
        counts["Total"] = counts["Gene"] + (counts["AHE"] + counts["UCE"])
        counts["specimen_id"] = specimen_id
        
        counts_list.append(counts)

# Create DataFrame from the counts list
counts_df = pd.DataFrame(counts_list)

# Reorder the columns
counts_df = counts_df[["file name", "specimen_id", "AHE", "UCE", "Gene", "Total"]]

# Save DataFrame to CSV
output_csv = "PRG_stats.csv"
counts_df.to_csv(output_csv, index=False)

print("CSV file saved successfully called PRG_stats.csv in the dir you run this command.")
