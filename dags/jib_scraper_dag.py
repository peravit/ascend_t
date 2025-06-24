from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
sys.path.append('/opt/airflow')
from scraper.bs4_scraper_jib import scrape_jib_notebook
from plugins.df_to_excel import save_to_excel
from plugins.upload_gdrive import upload_to_gdrive


default_args = {
    "start_date": datetime(2024, 1, 1)
}

target_file_path = None
file_name  ="jib_notebook"

def run_scrape_jib(ti):
    df = scrape_jib_notebook()
    file_path = save_to_excel(df, file_name)
    ti.xcom_push(key="excel_path", value=file_path)
    print(f"Pushed file path: {file_path}")

def upload_task(ti):
    file_path = ti.xcom_pull(task_ids="scrape_jib", key="excel_path")
    if not file_path:
        raise ValueError("File path not found from XCom")
    upload_to_gdrive(file_path)

with DAG(
    dag_id="jib_scraper_dag",
    schedule_interval="0 7 * * *",
    default_args=default_args,
    catchup=False,
    tags=["jib", "scraper"]
) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_jib",
        python_callable=run_scrape_jib
    )

    upload_to_gdrive_task = PythonOperator(
    task_id="upload_to_gdrive",
    python_callable=upload_task
    )
scrape_task >> upload_to_gdrive_task