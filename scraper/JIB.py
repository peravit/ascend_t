
#######

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080") 
driver = webdriver.Chrome(options=chrome_options)
key_input = 'notebook'


try:
    driver.get("https://www.jib.co.th")

    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ตกลง')]"))
        )
        cookie_btn.click()
    except:
        pass

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div/div/div[3]/div/div[1]/form/div/input"))
    )
    search_input.clear()
    search_input.send_keys(key_input)

    search_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div/div/div[3]/div/div[1]/form/div/div/button[2]/span"))
    )
    search_btn.click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='promo_name']"))
    )

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    names = [el.text.strip() for el in driver.find_elements(By.XPATH, "//span[@class='promo_name']")]
    prices = [el.text.strip() for el in driver.find_elements(By.XPATH, "//p[contains(@class, 'price')]")]

    df = pd.DataFrame({"Name": names, "Price": prices})
    df.to_excel("jib_notebook.xlsx", index=False)

    print(df.head(10))

finally:
    driver.quit()

