import os
import argparse

parser = argparse.ArgumentParser(description="Clean up directory and put docs into according folder")
parser.add_argument("--path", type=str, default=".", help="Directory to clean")

args = parser.parse_args()
path = args.path

print(f"Cleaning {path}")

# get all documents from given directory
content = os.listdir(path)

# create a relative path from the file and the document
path_content = [os.path.join(path, doc) for doc in content]

# filter our directory content into a documents and folders list
docs = [doc for doc in path_content if os.path.isfile(doc)]
folders = [folder for folder in path_content if os.path.isdir(folder)]

# moved files counter
moved = 0
created_folders = []

print(f"Cleaning up {len(docs)} elements.")

def dir_exists(folder_path):
    return folder_path in folders or folder_path in created_folders

# go through all files and move them into according folders
for doc in docs:
    full_doc_path, filetype = os.path.splitext(doc)
    doc_path = os.path.dirname(full_doc_path)
    doc_name = os.path.basename(full_doc_path)

    if doc_name == "main.py" or doc_name.startswith("."):
        continue

    subfolder_path = os.path.join(path, filetype[1:].lower())

    # create the folder if not exists
    if dir_exists(subfolder_path) is False:
        try:
            os.mkdir(subfolder_path)
            created_folders.append(subfolder_path)
            print(f"Folder {subfolder_path} created.")
        except FileExistsError as err:
            print(f"Folder already exists {subfolder_path}... {err}")
    
    # get the new folder path and move the file
    new_doc_path = os.path.join(subfolder_path, doc_name) + filetype
    os.rename(doc, new_doc_path)
    moved += 1
    print(f"Moved file {doc_name}{filetype} to {filetype}")

print(f"Moved {moved} of {len(docs)} elements")
