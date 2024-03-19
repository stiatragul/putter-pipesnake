# Topo_test.py work in progress
## 2024-03-19
## The idea of this script is to combine SEGUL summary and pick out the alignments that have max. ntaxa and minimum missing data.
## Then concatenate those files 

import argparse
import subprocess
import pandas as pd
import os
import shutil

def run_pipeline(alignment_path, num_loci):
    # Step 1: Run segul to analyze alignment files
    subprocess.run(["segul", "align", "summary", "-d", alignment_path, "-f", "fasta", "-o", "segul_stat", "--prefix", "segul_output"])
    # subprocess.run(["segul", "-i", input_path, "-o", "tmp" "--prefix" "segul_output"])

    # Step 2: Read segul output CSV and sort by number of taxa and missing data
    with open('segul_stat/segul_output_locus_summary.csv', 'r') as csvfile:
        df = pd.read_csv(csvfile)
        sorted_df = df.sort_values(by=['ntax', 'missing_data'], ascending=[False, True])

        # Print top loci
        print(sorted_df[['path', 'ntax', 'missing_data']].head(num_loci))

        # Create new directory for subset of files that have max ntaxa and min missing data
        subset_dir = os.path.join(os.path.dirname(alignment_path) + "_subset")
        os.makedirs(subset_dir, exist_ok=True)

        # Copy top files to subset directory
        top_files = sorted_df['path'].head(num_loci)
        for file_path in top_files:
            shutil.copy(file_path, subset_dir)

    # Step 3: Run segul align concat with files from subset directory
    output_prefix = os.path.basename(subset_dir) + "_cat"
    subprocess.run(["segul", "align", "concat", "--dir", subset_dir, "--input-format", "fasta", "--output", "segul_cat", "--prefix", output_prefix, "--output-format", "fasta"])

    # Move all folders starting with "segul_" to a new folder
    topo_test_folder = os.path.join(os.path.dirname(alignment_path) + "_topotest")
    os.makedirs(topo_test_folder, exist_ok=True)
    for item in os.listdir('.'):
        if os.path.isdir(item) and item.startswith('segul_'):
            shutil.move(item, topo_test_folder)

    print("Awesome, the next step is to run iqtree2 -s <concatenated.fas> -p <concatenate.partition> -t Constraint_tree.tre --tree-fix   -T AUTO")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pipeline for subsetting and concatenating alignment files.')
    parser.add_argument('-i', '--input_path', type=str, help='Path to the input alignment files')
    parser.add_argument('-n', '--num_loci', type=int, default=10, help='Number of top loci to select (default is 10)')
    args = parser.parse_args()

    run_pipeline(args.input_path, args.num_loci)
