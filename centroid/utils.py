import os
import streamlit as st
from subprocess import Popen
from notebook import notebookapp
from webbrowser import open_new_tab

from notebook.services.contents.filemanager import FileContentsManager as FCM

def create_folder(folder_path, folder_name):
    complete_path = os.path.join(folder_path, folder_name)
    os.makedirs(complete_path, exist_ok=True)

def create_file(file_path, file_name):
    complete_path = os.path.join(file_path, file_name)
    open(complete_path, 'w').close()

def create_nb(path, nb_name):
    complete_path = os.path.join(path, nb_name)
    FCM().new(path=complete_path)

def open_as_notebooks(path, python_code_file):
    for file in python_code_file:
        complete_path = os.path.join(path, file)
        Popen(['jupyter', 'notebook', complete_path])
        dir = os.path.join(os.getcwd(), path)

        for nb_info in notebookapp.list_running_servers():
            print(nb_info['notebook_dir'], dir)
            if nb_info['notebook_dir']==dir:
                port = nb_info['port']
                token = nb_info['token']
                url = nb_info['url']
                open_new_tab(f"{url}?token={token}")
                break

def kill_nbs(path=None, refresh=False):
    running_nb_servers = notebookapp.list_running_servers()
    if running_nb_servers:
        if path is None:
            for nb_info in running_nb_servers:
                port = nb_info['port']
                Popen(['jupyter',  'notebook', 'stop', f'{port}'])
        else:
            for nb_info in running_nb_servers:
                if nb_info['notebook_dir']==path:
                    port = nb_info['port']
                    Popen(['jupyter', 'notebook', 'stop', f'{port}'])

        if refresh:
            st.experimental_rerun()


def get_num_instances(path):
    running_nb_servers = notebookapp.list_running_servers()
    if running_nb_servers:
        count = 0
        for nb_info in running_nb_servers:
            if nb_info['notebook_dir']==path:
                count += 1
    else:
        count = 0

    return count