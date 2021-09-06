import streamlit as st
import hydralit_components as hc

from home import home
from experiments import display_ipynb_plots

if __name__ =="__main__":
    st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

    menu_data = [
        {'id':'Experiments','icon':"☢️",'label':"Experiments"},
        {'id':'Workflow','icon':"♻️",'label':"Workflow"},
        {'id':'Deployment','icon':"📦",'label':"Deployment"}
    ]

    # we can override any part of the primary colors of the menu
    #over_theme = {'txc_inactive': '#FFFFFF','menu_background':'red','txc_active':'yellow','option_active':'blue'}
    over_theme = {
        'txc_inactive': '#FFFFFF',
        'menu_background': '#5058cc'
        }

    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        home_name='Home',
        override_theme=over_theme
        )

    if menu_id=="Home":
        home()
    elif menu_id=="Experiments":
        display_ipynb_plots()