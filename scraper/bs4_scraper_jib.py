import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.df_to_excel import save_to_excel


def scrape_jib_notebook(sub_path="web/product/product_search/0?str_search=notebook&cate_id[]="):
    url = f"https://www.jib.co.th/{sub_path}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    names = [tag.text.strip() for tag in soup.select("div.boxname span.promo_name")]
    prices = [tag.text.strip() for tag in soup.select("div.boxprice p.price_total")]

    df = pd.DataFrame({"Name": names, "Price": prices})
    return df


if __name__ == "__main__":
    df = scrape_jib_notebook()
    output_path = os.path.join(os.path.dirname(__file__), "jib_notebook.xlsx")
    save_to_excel(df, output_path)


