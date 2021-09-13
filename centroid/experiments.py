import streamlit as st
import streamlit.components.v1 as components
import os

from utils import load_yaml

def show_plots(
    col,
    dir_name, 
    selected_ipynb,
    title,
    load_cache
    ):
        with col:
            ipynb_path = os.path.join(dir_name, selected_ipynb)
            html_name = selected_ipynb.split('.')[0]

            try:
                if not load_cache:
                    os.system(
                        f"jupyter nbconvert --to html --no-input {ipynb_path} --output {html_name}.html"
                        )

                with open(os.path.join(dir_name, f"{html_name}.html")) as f:
                    st.info(title)
                    components.html(
                        f.read(),
                        height=500,
                        scrolling=True
                        )

            except Exception as e:
                if isinstance(e, FileNotFoundError) and load_cache:
                    st.error(f"No cache found for {selected_ipynb}")
                else:
                    st.error(f"An error occured while fetching the plots from {selected_ipynb}")


def display_ipynb_plots():
    config = load_yaml(os.path.join('centroid_dashboard', 'config.yaml'))
    config_exp = config['EXP']

    cwd = os.getcwd()
    dir_name = config_exp['folder']
    deafult_option = 'None'

    col1, col2 = st.columns([1, 3])

    ipynb_files = [dir for dir in os.listdir(dir_name) if dir.split('.')[-1]=='ipynb']
    title = "All outputs inside the selected Jupyter notebook will be displayed here"

    if ipynb_files:
        with col1:
            selected_ipynb = st.selectbox(
                    label="Select a jupyter notebook to view outputs",
                    options=[deafult_option]+ipynb_files
                )
            load_cache = st.checkbox("Load from cache", value=True)

            if selected_ipynb!=deafult_option:
                show_plots(
                        col=col2,
                        dir_name=dir_name, 
                        selected_ipynb=selected_ipynb,
                        title=title,
                        load_cache=load_cache
                )
            else:
                with col2:
                    st.info(title)
            
    else:
        st.error("⚠️ No Jypter notebooks 📓 found in experiments folder")