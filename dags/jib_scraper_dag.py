from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import time
import pandas as pd
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


def scrape_jib_notebook():
    chrome_options = Options()
    chrome_options.binary_location = "/opt/chrome/chrome"  # 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 
    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    try:
        service = Service(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        key_input = 'notebook'
        driver.get("https://www.jib.co.th")

        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ตกลง')]"))
            )
            cookie_btn.click()
        except:
            pass  #  

        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_input.clear()
        search_input.send_keys(key_input)

        search_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-search')]"))
        )
        search_btn.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='promo_name']"))
        )

 
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        names = [el.text.strip() for el in driver.find_elements(By.XPATH, "//span[@class='promo_name']")]
        prices = [el.text.strip() for el in driver.find_elements(By.XPATH, "//p[contains(@class, 'price')]")]

        df = pd.DataFrame({"Name": names, "Price": prices})
        df.to_excel("/opt/airflow/dags/jib_notebook.xlsx", index=False)

        print("✅ Scraped:", df.shape[0], "rows")
        print(df.head(10))

    except Exception as e:
        print("❌ Error during scraping:", e)
        raise
    finally:
        driver.quit()


# ---------- DAG Definition ----------
default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    dag_id='jib_scraper_dag',
    schedule_interval='0 7 * * *',
    default_args=default_args,
    catchup=False,
    tags=['jib', 'selenium', 'scraping'],
) as dag:

    scrape_task = PythonOperator(
        task_id='scrape_notebook_from_jib',
        python_callable=scrape_jib_notebook,
    )
