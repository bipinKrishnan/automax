import streamlit as st
import os 

def workflow():
    prod_col, tests_col = st.columns(2)
    default_multiselect = "None"
    display_content = {
        'src': {
            'col': prod_col,
            'title': "Run production code workflow",
            'multiselect_text': "Select the order of the workflow"
        },
        'tests': {
            'col': tests_col,
            'title': 'Run unit testing code',
            'multiselect_text': "Select the tests you wish to skip"
        }
    }

    for i, key in enumerate(display_content.keys()):
        cwd = os.path.join(os.getcwd(), key)
        content_info = display_content[key]
        files = [f for f in os.listdir(cwd) if f.split('.')[-1]=='py']

        with content_info['col']:
            st.write(f"**{content_info['title']}**")
            st.multiselect(
                label=content_info['multiselect_text'], 
                options=files, 
                )
            st.button('Run', key=f"b'{i}'")