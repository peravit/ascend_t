import pandas as pd

output = '/opt/airflow/data_staging/'

def save_to_excel(df, filename):
    df.to_excel(output+filename, index=False)
    print(f"save {len(df)} rows to {filename}")
