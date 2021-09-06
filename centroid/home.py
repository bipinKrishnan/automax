import streamlit as st
import os
from functools import partial
import webbrowser

def home():
    exp_col, src_col, tests_col = st.columns(3)

    display_content = {
        'experiments': {'col': exp_col, 'label': 'Experiment notebooks', 'ext': 'ipynb'},
        'src': {'col': src_col, 'label': 'Production code', 'ext': 'py'},
        'tests': {'col': tests_col, 'label': 'Unit tests', 'ext': 'py'}
    }

    for key in display_content.keys():
        content_info = display_content[key]
        files = [f for f in os.listdir(key) if f.split('.')[-1]==content_info['ext']]

        with content_info['col']:
            selected_file = st.selectbox(label=content_info['label'], options=files)
    