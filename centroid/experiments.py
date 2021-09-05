import streamlit as st
import streamlit.components.v1 as components

import os 
from functools import partial

def show_plots(
    col,
    dir_name, 
    selected_ipynb,
    load_cache
    ):
        with col:
            ipynb_path = os.path.join(dir_name, selected_ipynb)
            html_name = selected_ipynb.split('.')[0]

            if not load_cache:
                os.system(
                    f"jupyter nbconvert --to html --no-input {ipynb_path} --output {html_name}.html"
                    )

            try:        
                with open(os.path.join(dir_name, f"{html_name}.html")) as f:
                    components.html(
                        f.read(),
                        height=500,
                        scrolling=True
                        )
            except FileNotFoundError:
                st.error(f"No cache found for {selected_ipynb}")

def display_ipynb_plots():
    cwd = os.getcwd()
    dir_name = 'experiments'
    col1, col2 = st.columns([1, 3])

    ipynb_files = [dir for dir in os.listdir(dir_name) if dir.split('.')[-1]=='ipynb']

    if ipynb_files:
        with col1:
            selected_ipynb = st.selectbox(
                    label="Select ipynb files to view plots",
                    options=ipynb_files
                )

            if selected_ipynb:
                load_cache = st.checkbox("Load from cache", value=True)
                st.button(
                    'Show plots',
                    on_click=partial(
                        show_plots,
                        col=col2,
                        dir_name=dir_name, 
                        selected_ipynb=selected_ipynb,
                        load_cache=load_cache
                    )
                )  
            
    else:
        st.error("⚠️ No Jypter notebooks 📓 found in experiments folder")