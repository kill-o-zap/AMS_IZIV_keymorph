import os
import numpy as np
import nibabel as nib
from scipy.ndimage import zoom

def process_npy_to_nii_with_custom_name(base_dir, output_dir, original_shape):
    """
    Processes all .npy files in the specified directory structure and saves them directly 
    to the output directory with custom naming based on the base directory name.

    Parameters:
        base_dir (str): Path to the base directory containing the 'eval' folder.
        output_dir (str): Path to the output base directory where the .nii.gz files will be saved.
        original_shape (tuple): Original shape to resize back to (e.g., (256, 192, 192, 3)).
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the base directory name to adjust file naming
    base_name = os.path.basename(base_dir)
    print(f"Processing base directory: {base_name}")
    
    # Determine the suffix for the filenames based on the base directory name
    if "T1" in base_name:
        suffix = "0001"  # T1
    elif "PD" in base_name:
        suffix = "0002"  # PD
    else:
        suffix = "0000"  # Default if neither T1 nor PD is in the name
    
    # Path to the 'eval' subdirectory
    eval_dir = os.path.join(base_dir, "eval")
    if not os.path.exists(eval_dir):
        print(f"Eval directory does not exist at {eval_dir}")
        return
    
    # Traverse the 'eval' directory to find subfolders
    index = 11  # Start with 0011 for the first subfolder
    for subfolder in sorted(os.listdir(eval_dir)):  # Iterate through subfolders in 'eval'
        subfolder_path = os.path.join(eval_dir, subfolder)
        
        if os.path.isdir(subfolder_path):
            print(f"  Found subfolder: {subfolder}")
            
            # Loop through the .npy files in the subfolder
            files_in_subfolder = [file for file in os.listdir(subfolder_path) if file.endswith(".npy") and file.startswith("grid_")]
            if not files_in_subfolder:
                print(f"    No grid_*.npy files found in {subfolder_path}")
            
            for i, file in enumerate(files_in_subfolder):  # Iterate through files in the subfolder
                if "-rot0-affine.npy" in file:
                    file_path = os.path.join(subfolder_path, file)
                    print(f"    Processing file: {file}")
                    
                    # Load the .npy file
                    data = np.load(file_path)
                    
                    # Compute reverse scaling factors
                    reverse_factors = [original_shape[i] / data.shape[i] for i in range(3)] + [1]
                    
                    # Resize the data to the original shape
                    resized_data = zoom(data, reverse_factors, order=1)  # Linear interpolation
                    
                    # Preserve RGB channels if they exist
                    if resized_data.shape[-1] == 3:
                        print("    Keeping RGB channels for NIfTI format.")
                    
                    # Create NIfTI image
                    affine = np.eye(4)  # Identity matrix for affine
                    nii_image = nib.Nifti1Image(resized_data, affine)
                    
                    # Generate custom filename based on the index and suffix
                    first_number = str(index).zfill(4)  # Incremented for each subfolder (e.g., '0011', '0012')
                    second_number = str(index).zfill(4)  # Same as first_number
                    filename = f"disp_{first_number}_{suffix}_{second_number}_0000.nii.gz"
                    
                    # Save the .nii.gz file directly in the output directory
                    output_file = os.path.join(output_dir, filename)
                    nib.save(nii_image, output_file)
                    print(f"    Saved as: {output_file}")
                    
                    # Load the saved NIfTI file to confirm its shape
                    saved_img = nib.load(output_file)
                    saved_data = saved_img.get_fdata()
                    print(f"    Shape of the saved NIfTI file ({output_file}): {saved_data.shape}")
                    
                    # Optionally, print file size on disk (in bytes)
                    file_size = os.path.getsize(output_file)
                    print(f"    Size of the saved NIfTI file ({output_file}): {file_size / 1024:.2f} KB")
                    
                    index += 1  # Increment the index for the next subfolder

# Example usage
base_directory_T1 = "registracija_T2m_T1f"  # Replace with your T1 directory path
base_directory_PD = "registracija_T2m_PDf"  # Replace with your PD directory path
output_directory = "deformacije"  # Replace with your desired output directory path
original_shape = (256, 192, 192, 3)  # Original shape to resize back to

# Process T1 data
process_npy_to_nii_with_custom_name(base_directory_T1, output_directory, original_shape)

# Process PD data
process_npy_to_nii_with_custom_name(base_directory_PD, output_directory, original_shape)
