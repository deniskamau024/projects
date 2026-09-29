import os
import shutil
# defne the folder you want to clean up
# for testing its's safe to create a testing folder named 'TestFolder'
TARGET_DIR = "./TestFolder"
TRACKED_EXTENSIONS = {
    "Images":[".jpg",".jpeg",".pnp",".gif",".webp"],
    "Documents": [".pdf",".docx",".txt",".xlsx",".pptx"],
    "Videos": [".mp4",".mov",".avi",".mkv"],
    "Audio": [".mp3",".wav",".flac"]
}

def clean_folder():
    #Make sure target folder exists.
    if not os.path.exists(TARGET_DIR):
        print(f"The folder '{TARGET_DIR}', does not exist.Please create it first!")
        return

    # Loop through every file in the folder.
    for filename in os.listdir(TARGET_DIR):
        # get full path of the item
        file_path = os.path.join(TARGET_DIR,filename)

        # Skip if it's a folder (we only want to move loose files)
        if os.path.isdir(file_path):
            continue

        # 4. Extract the file extension (and convert to lowercase)
        # os.path.splitext("photo.jpg") splits into ('photo', '.jpg')
        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        # 5. Figure out where the file belongs
        moved = False
        for folder_name, extensions_list in TRACKED_EXTENSIONS.items():
            if extension in extensions_list:
                # Define the path for the new sub-folder (e.g., ./TestFolder/Images)
                destination_folder = os.path.join(TARGET_DIR, folder_name)
                
                # Create the sub-folder if it doesn't exist yet
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                # Move the file
                new_destination = os.path.join(destination_folder, filename)
                shutil.move(file_path, new_destination)
                print(f"Moved: {filename} ➔ {folder_name}/")
                moved = True
                break

        # Optional: Handle unknown file types
        if not moved:
            print(f"Skipped unknown file type: {filename}")

if __name__ == "__main__":
    print("Starting file organization...")
    clean_folder()
    print("Done!") 