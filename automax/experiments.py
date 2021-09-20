from genericpath import exists
import streamlit as st 
import streamlit.components.v1 as components
import os 
from functools import partial 

import pandas as pd 
from pandas_profiling import ProfileReport
from pycaret import regression, classification

from utils import load_yaml


def get_profile_report(dataset, load_cache):
    config = load_yaml(os.path.join('automax_dashboard', 'config.yaml'))
    ds_file = os.path.join(
        config['OTHERS']['folders_to_create']['data_folder'], 
        dataset
        )

    df = pd.read_csv(ds_file)
    
    report_output_file = os.path.join(
        os.getcwd(),
        config['OTHERS']['cache_folder'],
        'dataset_profile',
        f"{dataset.replace('.csv', '')}.html"
        )

    if not load_cache:
        os.makedirs(os.path.dirname(report_output_file), exist_ok=True)
        design_report = ProfileReport(df)
        design_report.to_file(output_file=report_output_file) 

    try:
        with open(report_output_file) as f:
            components.html(
                f.read(),
                height=500,
                scrolling=True
                )
    except FileNotFoundError:
        st.info(f"No cache found for {dataset}")

def get_baselines(df, task, target):
    if task=='Regression':
        module = regression
    elif task=='Classification':
        module = classification

    clf = module.setup(data=df, target=target, silent=True)
    module.compare_models(verbose=False)
    out_df = pd.DataFrame(module.pull()) 

    st.dataframe(out_df)
    
def show_experiments():
    config = load_yaml(os.path.join('automax_dashboard', 'config.yaml'))
    data_folder = config['OTHERS']['folders_to_create']['data_folder']
    data_files = os.listdir(data_folder)
    csv_files = [f for f in data_files if f.split('.')[-1]=='csv']

    if csv_files==[]:
        st.info(
            f"Add the dataset in csv format to '{data_folder}' folder for generating data profile and baselines"
            )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("**Dataset profile**")
        report_dataset = st.selectbox(
            label="Select csv file", 
            options=csv_files, key=f"b'{2}'"
            )

        load_cache_reports = st.checkbox('Load from cache', value=True, key=f"b'{1}'")

        if report_dataset:
            get_profile_report(
                dataset=report_dataset,
                load_cache=load_cache_reports
                )

    with col2:
        st.write('**Baselines**')

        baseline_dataset = st.selectbox(
            label="Select csv file", 
            options=csv_files, 
            key=f"b'{3}'"
            )

        task_type = st.selectbox(
            label="Task",
            options=['Classification', 'Regression']
        )

        if baseline_dataset:
            ds_file = os.path.join(
                config['OTHERS']['folders_to_create']['data_folder'], 
                baseline_dataset
                )
            df = pd.read_csv(ds_file)
            df_columns = df.columns

        if baseline_dataset:
            target = st.selectbox(label='Select target column', options=df_columns)
            show_baselines = st.button(label="Show baselines")
            if show_baselines:
                get_baselines(
                    df=df, 
                    task=task_type,
                    target=target,
                    )