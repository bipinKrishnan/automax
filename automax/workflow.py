from json import load
import streamlit as st
import os 
import subprocess
from functools import partial
from datetime import datetime

from utils import load_yaml

def check_script_args():
    config = load_yaml(os.path.join('automax_dashboard', 'config.yaml'))
    args_file = config['OTHERS']['script_args_file']
    if not os.path.exists(args_file):
        open(args_file, 'w').close()

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

def run_scripts(key, selected_files, logs_folder):
    config = load_yaml(os.path.join('automax_dashboard', 'config.yaml'))

    if key==config['SRC']['folder']:
        args = check_script_args()
        src_log_file = config['SRC']['log_file']
        src_log = open(os.path.join(logs_folder, src_log_file), 'w')

        for file in selected_files:
            current_script = os.path.join(key, file)

            if file in args.keys():
                subprocess.Popen(
                    ["python3", f"{current_script}", f"'{args[file]}'"],
                    stdout=src_log, stderr=src_log
                    )
            else:
                subprocess.Popen(
                    ["python3", f"{current_script}"],
                    stdout=src_log, stderr=src_log
                    )

    elif key==config['TESTS']['folder']:
        test_log_file = config['TESTS']['log_file']
        test_log = open(os.path.join(logs_folder, test_log_file), 'w')
        test_command = ['pytest', '-v']

        for test in os.listdir(key):
            if (not test in selected_files) and (test!='__pycache__'):
                test_command.append(os.path.join(key, test))

        subprocess.Popen(test_command, stdout=test_log, stderr=test_log)
    

def workflow():
    config = load_yaml(os.path.join('automax_dashboard', 'config.yaml'))
    config_src = config['SRC']
    config_tests = config['TESTS']
    config_others = config['OTHERS']
    logs_folder = os.path.join(
        os.getcwd(), 
        config_others['cache_folder'], 
        config_others['logs_folder']
        )

    os.makedirs(logs_folder, exist_ok=True)

    prod_col, tests_col = st.columns(2)
    display_content = {
        config_src['folder']: {
            'col': prod_col,
            'title': "Run production code workflow",
            'multiselect_text': "Select the order of the workflow",
            'button_text': 'Run workflow'
        },
        config_tests['folder']: {
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

            if key==config_src['folder']:
                help = "If there are arguments for any scripts, store it in 'script_arguments' file"
            elif key==config_tests['folder']:
                help = ""

            selected_files = st.multiselect(
                    label=content_info['multiselect_text'], 
                    options=files, 
                    help=help
                    )
            run_button = st.button(
                content_info['button_text'],
                on_click=partial(
                    run_scripts, 
                    key=key, 
                    selected_files=selected_files,
                    logs_folder=logs_folder
                    )
                )

            st.write('--------------')
            st.text('Output')
            st.button('⟳', key=key)

            if key==config_src['folder']:
                log_path = os.path.join(logs_folder, config_src['log_file'])
            elif key==config_tests['folder']:
                log_path = os.path.join(logs_folder, config_tests['log_file'])

            try:
                with open(log_path, 'r') as f:
                    content = f.read()

                if content!="":
                    m_time = datetime.fromtimestamp(
                        os.path.getmtime(log_path)
                        )
                    st.code(f"[+]Output logged at {m_time}\n{'-'*20}\n\n{content}")

            except FileNotFoundError:
                st.code("")

                