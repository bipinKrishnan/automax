import streamlit as st 
import streamlit.components.v1 as components
import os 

from utils import load_yaml

def show_pandas_profile_report():
    with open(f"../report.html") as f:
        components.html(
            f.read(),
            height=500,
            scrolling=True
            )

def show_experiments():
    config = load_yaml(os.path.join('automax_dashboard', 'config.yaml'))
    data_files = os.listdir(config['OTHERS']['folders_to_create']['data_folder'])