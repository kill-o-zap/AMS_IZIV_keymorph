import os
import shutil

# Define constants
OUTPUT_FOLDER_TRAINING = "data_prepared/centered_IXI"      # IDs below 0011, training data
OUTPUT_FOLDER_VALIDATION = "data_prepared/validation_data"  # IDs 0011 and onward, val data
SUBFOLDERS = {
    "0000": "T2",
    "0001": "T1",
    "0002": "PD"
}

# Create the output directory structure
def create_output_folders():
    for folder in [OUTPUT_FOLDER_TRAINING, OUTPUT_FOLDER_VALIDATION]:
        for key in SUBFOLDERS.values():
            os.makedirs(os.path.join(folder, key), exist_ok=True)
            os.makedirs(os.path.join(folder, f"{key}_mask"), exist_ok=True)

# Determine which output folder to use based on the patient ID
def get_output_folder(person_id):
    if int(person_id) >= 11:  # IDs 0011 and onward
        return OUTPUT_FOLDER_VALIDATION
    else:  # IDs below 0011
        return OUTPUT_FOLDER_TRAINING

# Rename and move files to the appropriate folder
def organize_files(input_image_folder, input_mask_folder):
    for folder, is_mask in [(input_image_folder, False), (input_mask_folder, True)]:
        for filename in os.listdir(folder):
            if not filename.endswith(".nii.gz"):
                print(f"Skipping {filename}: not a .nii.gz file.")
                continue

            try:
                # Split and parse filename
                base_name, ext = os.path.splitext(filename)
                base_name, ext2 = os.path.splitext(base_name)
                if ext2 != ".nii":
                    print(f"Skipping {filename}: unexpected extension structure.")
                    continue

                parts = base_name.split("_")
                if len(parts) < 3:
                    print(f"Skipping {filename}: unexpected naming structure.")
                    continue

                person_id = parts[1]  # Extract person ID (e.g., "0013")
                subfolder_key = parts[2]  # Extract type (e.g., "0000", "0001", "0002")
                subfolder_name = SUBFOLDERS.get(subfolder_key, None)

                if not subfolder_name:
                    print(f"Skipping {filename}: unknown subfolder key {subfolder_key}.")
                    continue

                # Determine output subfolder and new filename
                output_base_folder = get_output_folder(person_id)
                output_subfolder = f"{subfolder_name}_mask" if is_mask else subfolder_name
                new_filename = f"{parts[0]}_{person_id}"
                if is_mask:
                    new_filename += "_mask"
                new_filename += ".nii.gz"

                # Move the file
                source_path = os.path.join(folder, filename)
                dest_path = os.path.join(output_base_folder, output_subfolder, new_filename)

                shutil.copy2(source_path, dest_path)
                print(f"Moved {source_path} -> {dest_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Main execution flow
if __name__ == "__main__":
    # Poti do map s slikami
    input_image_folder = "ThoraxCBCT_OncoRegRelease_06_12_23/Release_06_12_23/imagesTr"
    input_mask_folder = "ThoraxCBCT_OncoRegRelease_06_12_23/Release_06_12_23/masksTr"

    # Create output folder structure
    create_output_folders()

    # Organize files
    organize_files(input_image_folder, input_mask_folder)

    print("File organization complete.")