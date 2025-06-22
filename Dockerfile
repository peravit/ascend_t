FROM apache/airflow:2.7.1

USER root

RUN apt-get update && \
    apt-get install -y wget unzip curl gnupg \
        libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
        libxss1 libappindicator1 libasound2 libxtst6 libxrandr2 \
        fonts-liberation libappindicator3-1 xdg-utils \
        --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget -O /tmp/chrome.zip https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chrome-linux64.zip && \
    unzip /tmp/chrome.zip -d /opt/ && \
    mv /opt/chrome-linux64 /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm /tmp/chrome.zip

RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    mv /opt/chromedriver-linux64 /opt/chromedriver && \
    ln -s /opt/chromedriver/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm /tmp/chromedriver.zip

USER airflow

RUN pip install --no-cache-dir \
    pandas==2.0.3 \
    selenium==4.27.1 \
    openpyxl==3.1.5 \
    matplotlib==3.7.5 \
    beautifulsoup4==4.13.4 \
    xlsxwriter==3.2.3 \
    dataframe_image==0.2.7 \
    SQLAlchemy==1.4.49

USER airflow
