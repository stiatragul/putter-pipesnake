import argparse
import os
import pandas as pd

def filter_files(combined_metadata_path, sample_info_path, quality_threshold):
    # Read CSV files into pandas DataFrames
    combined_metadata_df = pd.read_csv(combined_metadata_path)
    sample_info_df = pd.read_csv(sample_info_path)

    # Filter combined_metadata based on quality > threshold
    filtered_combined_metadata = combined_metadata_df[combined_metadata_df['total file size (mb)'] > quality_threshold]

    # Extract sample_ids from filtered_combined_metadata
    filtered_sample_ids = filtered_combined_metadata['sample_id']

    # Identify the Sample IDs that are kept in sample_info
    kept_sample_info = sample_info_df[sample_info_df['sample_id'].isin(filtered_sample_ids)]

    # Identify the rows to be discarded in BPA_combined
    discarded_bpa_combined = combined_metadata_df[~combined_metadata_df['sample_id'].isin(filtered_sample_ids)]

    # Generate output file names based on input names and threshold
    base_combined_metadata, ext_combined_metadata = os.path.splitext(os.path.basename(combined_metadata_path))
    base_sample_info, ext_sample_info = os.path.splitext(os.path.basename(sample_info_path))
    output_discarded_bpa_combined = f"BPA_combined_discarded{quality_threshold}.csv"

    # output_combined_metadata = f"{base_combined_metadata}_filtered{quality_threshold}{ext_combined_metadata}"
    output_kept_sample_info = f"{base_sample_info}_kept{quality_threshold}mb{ext_sample_info}"

    # Save the results to new CSV files
    # filtered_combined_metadata.to_csv(output_combined_metadata, index=False, columns=['sample_id'])
    kept_sample_info.to_csv(output_kept_sample_info, index=False)
    discarded_bpa_combined.to_csv(output_discarded_bpa_combined, index=False)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter CSV files based on quality > threshold")
    parser.add_argument("combined_metadata_file", help="Path to the Combined_meta_data CSV file")
    parser.add_argument("sample_info_file", help="Path to the SampleInfo CSV file")
    parser.add_argument("--threshold", type=int, default=100, help="Quality threshold value in mb (default is 100mb)")

    args = parser.parse_args()

    filter_files(args.combined_metadata_file, args.sample_info_file, args.threshold)
