import os 

def create_folder(folder_path, folder_name):
    complete_path = os.path.join(folder_path, folder_name)
    os.makedirs(complete_path, exist_ok=True)

def create_file(file_path, file_name):
    complete_path = os.path.join(file_path, file_name)
    open(complete_path, 'w').close()