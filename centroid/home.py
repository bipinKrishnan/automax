import streamlit as st
import os
from functools import partial

from utils import create_file


def home():
    exp_col, src_col, tests_col = st.columns(3)

    display_content = {
        'experiments': {
            'col': exp_col, 
            'label': 'Experiment notebooks 📓', 
            'ext': 'ipynb',
            'text_input': 'Enter the notebook name(include .ipynb extension)'
            },
        'src': {
            'col': src_col, 
            'label': 'Production code 🚢', 
            'ext': 'py',
            'text_input': 'Enter the file name with extension'
            },
        'tests': {
            'col': tests_col, 
            'label': 'Unit tests 📝', 
            'ext': 'py',
            'text_input': 'Enter the file name(include .py extension)'
            }
    }

    for i, key in enumerate(display_content.keys()):
        content_info = display_content[key]
        files = [f for f in os.listdir(key) if f.split('.')[-1]==content_info['ext']]

        with content_info['col']:
            st.write(content_info['label'])
            with st.expander(label="Add files"):
                file_name = st.text_input(
                                label=content_info['text_input']
                                )

                if file_name:
                    if os.path.exists(os.path.join(key, file_name)):
                        st.markdown(f"File **{file_name}** exists")
                    else:
                        create_file(key, file_name)
                        st.markdown(f"Created **{file_name}**")

            # TODO: clear text input when enter key is pressed
            st.markdown(f"ℹ️ Only ** *.{content_info['ext']}** files are shown")
            for f in files:
                st.write(f"[{f}](google.com)")
    
    