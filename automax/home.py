import streamlit as st
import os
from functools import partial
from notebook import notebookapp
import seedir as sd

from utils import load_yaml

from utils import (
    create_file, 
    kill_nbs, 
    open_as_notebooks, 
    create_nb,
    get_num_instances,
)


def home():
    config = load_yaml(os.path.join('automax_dashboard', 'config.yaml'))
    exp_col, src_col, tests_col = st.columns(3)

    display_content = {
        'experiments': {
            'col': exp_col, 
            'label': 'Experiment notebooks 📓', 
            'ext': 'ipynb',
            'text_input': 'Enter the notebook name(include .ipynb extension)',
            'file_label': 'notebook',
            'folder_name': config['OTHERS']['folders_to_create']['exp_folder']
            },
        'src': {
            'col': src_col, 
            'label': 'Production code 🚢', 
            'ext': 'py',
            'text_input': 'Enter the file name(include extension)',
            'file_label': 'script',
            'folder_name': config['OTHERS']['folders_to_create']['code_folder']
            },
        'tests': {
            'col': tests_col, 
            'label': 'Unit tests 📝', 
            'ext': 'py',
            'text_input': 'Enter the name of the test(include .py extension)',
            'file_label': 'test',
            'folder_name': config['OTHERS']['folders_to_create']['tests_folder']
            }
    }

    for i, key in enumerate(display_content.keys()):
        content_info = display_content[key]
        files = [f for f in os.listdir(key) if f.split('.')[-1]==content_info['ext']]
        cwd = os.path.join(os.getcwd(), key)

        with content_info['col']: 
            st.write(f"**{content_info['label']}**")

            with st.expander(label=f"Create new file"):
                file_name = st.text_input(
                                label=content_info['text_input'],
                                help=f"Created files will be stored in '{key}' directory"
                                )
                file_create = st.button('Create', key=f"b'{i}'")

            if file_create:
                if os.path.exists(os.path.join(key, file_name)):
                    st.info(f"File {file_name} exists")
                else:
                    if key=='experiments':
                        create_nb(key, file_name)
                    else:
                        create_file(key, file_name)
                    st.experimental_rerun()

            with st.expander(label=f"Open files"):
                if not files:
                    st.info(f"No .{content_info['ext']} files found, first create one.")
                else:
                    files_to_open = st.multiselect(
                        f"Select {content_info['file_label']}s to open", 
                        files
                        )
                    st.button(
                        'Open', key=str(i), on_click=partial(
                        open_as_notebooks, 
                        path=key, 
                        python_code_file=files_to_open
                        )
                    )

            st.write('------------------')

            running_nb_servers = [nb_info for nb_info in notebookapp.list_running_servers() if nb_info['notebook_dir']==cwd]

            st.text(f"Jupyter instances running 🏃: {get_num_instances(cwd)}")
            if running_nb_servers:
                a = st.button(
                    "Stop all", 
                    on_click=partial(kill_nbs, path=cwd), 
                    key=key
                    )

            st.code(
                f"Directory structure\n\n{sd.seedir(content_info['folder_name'], style='emoji', indent=3, printout=False)}"
                )