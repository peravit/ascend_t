import pandas as pd
import os
from datetime import datetime

output = '/opt/airflow/data_staging/'

def save_to_excel(df, filename_base):
    today_str = datetime.today().strftime("%Y%m%d")
    filename = f"{filename_base}_{today_str}.xlsx"
    full_path = os.path.join(output, filename)

    df.to_excel(full_path, index=False)
    print(f"Saved {len(df)} rows to {full_path}")
    
    return full_path