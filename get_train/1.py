import os
import shutil

source_dir = "img"
destination_dir = "img1"

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

files = os.listdir(source_dir)

for i, name in enumerate(files):
    source_file = os.path.join(source_dir, name)
    destination_file = os.path.join(destination_dir, f"{str(i+1).zfill(4)}.png")

    shutil.copy(source_file, destination_file)

    print(f"Copied {source_file} to {destination_file}")
