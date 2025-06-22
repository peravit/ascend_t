FROM apache/airflow:2.7.1

USER airflow
 
RUN pip install --no-cache-dir \
    matplotlib==3.7.5 \
    openpyxl==3.1.5 \
    xlsxwriter==3.2.3 \
    dataframe_image==0.2.7 \
    zipfile36==0.1.3 \
    SQLAlchemy==1.4.49 \
    pandas==2.0.3