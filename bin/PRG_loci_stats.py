import os
import sys
import pandas as pd

# Function to count sample headers in a fasta file
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

# Iterate through fasta files in the directory
for filename in os.listdir(fasta_directory):
    if filename.endswith(".fasta"):  # Assuming fasta file extension is .fasta
        file_path = os.path.join(fasta_directory, filename)
        counts = count_sample_headers(file_path)
        counts["file name"] = filename
        counts["Total"] = counts["Gene"] + (counts["AHE"] + counts["UCE"])
        counts_list.append(counts)

# Create DataFrame from the counts list
counts_df = pd.DataFrame(counts_list)

# Reorder the columns
counts_df = counts_df[["file name", "AHE", "UCE", "Gene", "Total"]]

# Save DataFrame to CSV
output_csv = "PRG_stats.csv"
counts_df.to_csv(output_csv, index=False)

print("CSV file saved successfully kak.")
