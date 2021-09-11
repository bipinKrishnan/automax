import streamlit as st
import os 
from functools import partial


def check_script_args():
    args_file = 'script_arguments'
    script_info_dict = {}

    if os.path.getsize(args_file)>0:
        with open(args_file, 'r') as f:
            content = f.read()
        
        for line in content.split('\n'):
            if line!="":
                script_name, args = line.split('=')
                script_name, args = script_name.strip(), args.strip()
                script_info_dict[script_name] = args

    return script_info_dict

def run_scripts(key, selected_files):
    if key=='src':
        args = check_script_args()
        for file in selected_files:
            current_script = os.path.join(key, file)

            if file in args.keys():
                res = os.system(f"python3 {current_script} {args[file]}")
            else:
                res = os.system(f"python3 {current_script}")
    elif key=='tests':
        tests_to_run = ' '.join(
            [
                (os.path.join(key, test)) for test in os.listdir(key) if not test in selected_files
            ]
        )
        res = os.system(f"pytest -v {tests_to_run}")

def workflow():
    prod_col, tests_col = st.columns(2)
    default_multiselect = "None"
    display_content = {
        'src': {
            'col': prod_col,
            'title': "Run production code workflow",
            'multiselect_text': "Select the order of the workflow",
            'button_text': 'Run workflow'
        },
        'tests': {
            'col': tests_col,
            'title': 'Run unit tests',
            'multiselect_text': "Select the tests you wish to skip",
            'button_text': 'Run tests'
        }
    }

    for i, key in enumerate(display_content.keys()):
        cwd = os.path.join(os.getcwd(), key)
        content_info = display_content[key]
        files = [f for f in os.listdir(cwd) if f.split('.')[-1]=='py']

        with content_info['col']:
            st.write(f"**{content_info['title']}**")

            if key=='src':
                help = "If there are arguments for any scripts, store it in 'script_arguments' file"
            elif key=='tests':
                help = ""

            selected_files = st.multiselect(
                    label=content_info['multiselect_text'], 
                    options=files, 
                    help=help
                    )
            st.button(content_info['button_text'], on_click=partial(
                run_scripts, key=key, selected_files=selected_files)
            )