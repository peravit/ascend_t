from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

from scraper.bs4_scraper_jib import scrape_jib_notebook
from plugins.df_to_excel import save_to_excel

# def scrape_jib_notebook(sub_path="web/product/product_search/0?str_search=notebook&cate_id[]="):
#     url = f"https://www.jib.co.th/{sub_path}"
#     response = requests.get(url)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.text, "html.parser")

#     names = [tag.text.strip() for tag in soup.select("div.boxname span.promo_name")]
#     prices = [tag.text.strip() for tag in soup.select("div.boxprice p.price_total")]

#     df = pd.DataFrame({"Name": names, "Price": prices})
#     df.to_csv("/opt/airflow/data_staging/jib_notebook.csv", index=False)

# with DAG(
#     dag_id="scrape_jib_notebook",
#     start_date=datetime(2024, 1, 1),
#     schedule_interval="0 7 * * *",
#     catchup=False
# ) as dag:

#     scrape_task = PythonOperator(
#         task_id="scrape_jib",
#         python_callable=scrape_jib_notebook
#     )

default_args = {
    "start_date": datetime(2024, 1, 1)
}

def run_scrape_jib():
    df = scrape_jib_notebook()
    save_to_excel(df, "jib_notebook.xlsx")

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