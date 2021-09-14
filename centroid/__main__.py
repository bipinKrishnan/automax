from typer import run
import os
from shutil import copyfile

from utils import create_folder, create_file, load_yaml


def main(path_to_project, project_name):
    try:
        config = load_yaml('config.yaml')
        config_others = config['OTHERS']

        project_path = os.path.join(path_to_project, project_name)

        src_folder = config_others['src_folder_for_project']

        webapp_folder = config_others['webapp_folder']
        webapp_main_file = config_others['webapp_main_file']
        files_to_copy = config_others['files_to_copy']

        webapp_dst_path = os.path.join(project_path, webapp_folder)

        folders = config_others['folders_to_create']
        files = config_others['files_to_create']

        os.makedirs(project_path, exist_ok=True)
        for folder_name in folders:
            create_folder(project_path, folder_name)

        for file_name in files:
            create_file(project_path, file_name)
        
        os.makedirs(webapp_dst_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, config_others['cache_folder']), exist_ok=True)

        for f in files_to_copy:
            src_path = os.path.join(src_folder, f)
            dst_path = os.path.join(webapp_dst_path, f)
            copyfile(src_path, dst_path)

        config_file = 'config.yaml'
        copyfile(
            os.path.join(config_file), 
            os.path.join(project_path, webapp_folder, config_file)
            )

        os.system(
            f"cd {project_path} && streamlit run {os.path.join(webapp_folder, webapp_main_file)}"
            )   
    except KeyboardInterrupt:
        exit()

if __name__=="__main__":
    run(main)