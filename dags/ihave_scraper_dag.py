from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

from scraper.bs4_scraper_ihave import scrape_ihavecpu_notebook
from plugins.df_to_excel import save_to_excel

default_args = {
    "start_date": datetime(2024, 1, 1)
}

def run_scrape_ihave():
    df = scrape_ihavecpu_notebook()
    save_to_excel(df, "ihave_notebook.xlsx")

with DAG(
    dag_id="ihave_scraper_dag",
    schedule_interval="0 7 * * *",
    default_args=default_args,
    catchup=False,
    tags=["ihave", "scraper"]
) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_ihave",
        python_callable=run_scrape_ihave
    )
