import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.df_to_excel import save_to_excel

def scrape_ihavecpu_notebook(max_item=100):
    url = "https://apisp.ihavecpu.com/api/product/search"
    limit = 32
    offset = 0

    all_data = []

    while len(all_data) < max_item:
        payload = {
            "search": "notebook",
            "lang": "th",
            "field": "sell_price",
            "sort": "asc",
            "offset": offset,
            "limit": limit
        }

        response = requests.post(url, json=payload)
        data = response.json()

        products = data["res_result"]["data"]
        if not products:
            break  

        for p in products:
            all_data.append({
                "Name": p["name_th"],
                "Price": p["price_sale"]
            })
        
        print(f" เก็บครบ {len(all_data)} ชิ้น")

        if len(all_data) >= max_item:
            break

        offset += limit
        time.sleep(1)   

    df = pd.DataFrame(all_data[:max_item])   
    return df


if __name__ == "__main__":

    df = scrape_ihavecpu_notebook()
    output_path = os.path.join(os.path.dirname(__file__), "ihavecpu_notebook.xlsx")
    save_to_excel(df, output_path)
