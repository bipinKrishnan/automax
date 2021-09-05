import streamlit as st
import streamlit.components.v1 as components
import os 

def display_ipynb_plots():
    cwd = os.getcwd()
    dir_name = 'experiments'
    default_option = 'None'
    col1, col2 = st.columns([1, 3])

    ipynb_files = [dir for dir in os.listdir(dir_name) if dir.split('.')[-1]=='ipynb']

    if ipynb_files:
        with col1:
            selected_ipynb = st.selectbox(
                    label="Select ipynb files to view plots",
                    options=[default_option]+ipynb_files
                )
            load_cache = st.checkbox("Load from cache", value=True)

        with col2:
            if selected_ipynb!=default_option:
                ipynb_path = os.path.join(dir_name, selected_ipynb)
                html_name = selected_ipynb.split('.')[0]

                if not load_cache:
                    os.system(
                        f"jupyter nbconvert --to html --no-input {ipynb_path} --output {html_name}.html"
                        )
                        
                with open(os.path.join(dir_name, f"{html_name}.html")) as f:
                    components.html(
                        f.read(),
                        height=500,
                        scrolling=True
                        )
            
    else:
        st.error("⚠️ No Jypter notebooks 📓 found in experiments folder")