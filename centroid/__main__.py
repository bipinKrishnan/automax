from typer import run
import os
from shutil import copyfile

from utils import create_folder, create_file


def main(path_to_project, project_name):
    try:
        project_path = os.path.join(path_to_project, project_name)
        webapp_folder = "centroid_dashboard"
        webapp_main_file = 'app.py'
        files_to_copy = ['app.py', 'home.py', 'experiments.py', 'utils.py']
        webapp_dst_path = os.path.join(project_path, webapp_folder)

        folders = ['experiments', 'src', 'tests']
        files = ['README.md']

        os.makedirs(project_path, exist_ok=True)
        for folder_name in folders:
            create_folder(project_path, folder_name)

        for file_name in files:
            create_file(project_path, file_name)
        
        os.makedirs(webapp_dst_path, exist_ok=True)

        for f in files_to_copy:
            src_path = os.path.join('centroid', f)
            dst_path = os.path.join(webapp_dst_path, f)
            copyfile(src_path, dst_path)

        os.system(
            f"cd {project_path} && streamlit run {os.path.join(webapp_folder, webapp_main_file)}"
            )   
    except KeyboardInterrupt:
        exit()

if __name__=="__main__":
    run(main)