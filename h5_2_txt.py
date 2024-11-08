import h5py
import numpy as np
import argparse
import os

def save_dataset_to_txt(file_path):
    # Extract the base name of the file (without directory and extension)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Open the HDF5 file
    with h5py.File(file_path, "r") as hdf:
        # Iterate through all datasets in the file
        def visit_datasets(name, obj):
            if isinstance(obj, h5py.Dataset):
                # Read the dataset
                data = obj[:]

                # Construct the output file name
                output_file = f"{base_name}_{name.replace('/', '_')}.txt"

                # Save the dataset to a text file
                np.savetxt(output_file, data, fmt="%.6f")  # Adjust format if needed
                print(f"Dataset '{name}' saved to '{output_file}'")

        # Visit all datasets in the file
        hdf.visititems(visit_datasets)

if __name__ == "__main__":
    # Setup argparse for input file path
    parser = argparse.ArgumentParser(description="Extract datasets from an HDF5 file and save them as text files.")
    parser.add_argument("file", type=str, help="Path to the HDF5 file")
    args = parser.parse_args()

    # Call the function with the input file path
    save_dataset_to_txt(args.file)
