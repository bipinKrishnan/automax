import streamlit as st
import os


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
                                label=content_info['text_input'],
                                )
            # TODO: clear text input when enter key is pressed
            for f in files:
                st.text(f)
    