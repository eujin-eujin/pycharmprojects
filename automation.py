import os
import shutil

# Define the source and destination folders
root_dir = r'D:\Photos Eujin\Eujin Database'
source_folders = [os.path.join(root_dir,dir) for dir in os.listdir(root_dir)[1:]]
destination_folder = r"D:\Photos Eujin\Eujin Database\1"

# Iterate over the source folders and move everything to the destination folder
for source_folder in source_folders:
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            try:
                shutil.move(os.path.join(root,file), os.path.join(destination_folder, file))
            except Exception as e:
                print(e)

print("All files have been moved to the first folder.")
