FROM apache/airflow:2.7.1

USER root

RUN apt-get update && \
    apt-get install -y wget gnupg unzip curl \
    libasound2 libatk-bridge2.0-0 libgtk-3-0 libnss3 libxss1 libxrandr2 xdg-utils \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow


RUN pip install --no-cache-dir \
    pandas==2.0.3 \
    selenium==4.27.1 \
    openpyxl==3.1.5 \
    matplotlib==3.7.5 \
    beautifulsoup4==4.13.4 \
    xlsxwriter==3.2.3 \
    dataframe_image==0.2.7 \
    SQLAlchemy==1.4.49\
    requests==2.31.0\
    beautifulsoup4\
    PyDrive2==1.21.3