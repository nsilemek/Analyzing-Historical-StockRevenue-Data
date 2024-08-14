# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 21:41:10 2024

@author: user
"""
# !pip install yfinance==0.2.38
# !pip install pandas==2.2.2
# !pip install nbformat

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    
##Tesla    
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url)

soup = BeautifulSoup(html_data.content, 'html.parser')

tables = soup.findAll('table')
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for table in tables:
    if "Tesla Quarterly Revenue" in table.get_text():
        rows = table.find_all('tr')
        for row in rows[1:]:  
            cols = row.find_all('td')
            if len(cols) >= 2:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip()

                revenue_clean = revenue.replace('$', '').replace(',', '')

                new_row = pd.DataFrame({"Date": [date], "Revenue": [revenue_clean]})
                tesla_revenue = pd.concat([tesla_revenue, new_row], ignore_index=True)

        break  

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail()

make_graph(tesla_data,tesla_revenue,'Tesla')

##GameStop
gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period="max")
##gme_data.head()
gme_data.reset_index(inplace=True)
gme_data.head()

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(url).text

soup_2 = BeautifulSoup(html_data_2, 'html.parser')

tables = soup_2.findAll('table')
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for table in tables:
    if "GameStop Revenue" in table.get_text():
        rows = table.find_all('tr')
        for row in rows[1:]:  
            cols = row.find_all('td')
            if len(cols) >= 2:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip()

                revenue_clean = revenue.replace('$', '').replace(',', '')

                new_row = pd.DataFrame({"Date": [date], "Revenue": [revenue_clean]})
                gme_revenue = pd.concat([gme_revenue, new_row], ignore_index=True)

        break  
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)
gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

make_graph(gme_data,gme_revenue,'GameStop')

gme_data.tail()
