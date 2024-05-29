import streamlit as st
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go


# Title and Logo
st.markdown("<h1 style='text-align: center;'>AI Powered Stock Analysis</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.1.png")

st.sidebar.title("NavBar")

# Google Finance web scrapper
def fetch_stock_data(stock_symbol, exchange):
    url = f"https://www.google.com/finance/quote/{stock_symbol}:{exchange}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        try:
            stock_name = soup.find("div", class_="zzDege").text
        except AttributeError:
            stock_name = "N/A"
        try:
            current_price = soup.find("div", class_="YMlKec fxKbKc").text
        except AttributeError:
            current_price = "N/A"
        try:
            previous_close = soup.find("div", class_="P6K39c").text
        except AttributeError:
            previous_close = "N/A"
        try:
            stock_revenue = soup.find(class_="QXDnM").text
        except AttributeError:
            stock_revenue = "N/A"
        try:
            stock_news = soup.find(class_="Yfwt5").text
        except AttributeError:
            stock_news = "N/A"
        
        return {
            "Stock name": stock_name,
            "Current price": current_price,
            "Previous close": previous_close,
            "Stock revenue": stock_revenue,
            "Headline": stock_news
        }
    else:
        return None

# Sidebar 
#Current data
st.sidebar.subheader("Stock Data")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="")
exchange = st.sidebar.selectbox("Select Exchange", ["NASDAQ", "NSE", "BSE"])

if st.sidebar.button("Get Data"):
    data = fetch_stock_data(stock_symbol, exchange)
    
    if data:
        st.subheader("Stock Overview")
        df = pd.DataFrame([data], index=["Extracted data"]).T
        st.dataframe(df)
    else:
        st.write("Failed to retrieve data. Please check the stock symbol and exchange.") 

# Fetch historical data
def fetch_historical_data(ticker, interval, start_date, end_date):
    data = yf.download(ticker, interval=interval, start=start_date, end=end_date)
    return data

# historical data
st.sidebar.subheader("Fetch Historical Data")
ticker = st.sidebar.text_input('Enter Stock Symbol for Historical Data:')
interval = st.sidebar.selectbox('Select Interval:', ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1d', '1wk', '1mo', '3mo'])
start_date = st.sidebar.date_input('Start Date for Historical Data:')
end_date = st.sidebar.date_input('End Date for Historical Data:')

if st.sidebar.button('Get Historical Data'):
    if start_date and end_date:
        data = fetch_historical_data(ticker, interval, start_date, end_date)
        if not data.empty:
            st.subheader(f'Stock Historical Data for {ticker}')
            st.write(f'From {start_date} to {end_date} at {interval} interval')
            st.dataframe(data)

            # Plotting with plotly
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'],
                                         name='market data'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(200).mean(), mode='lines', name='SMA 200'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(50).mean(), mode='lines', name='SMA 50'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(20).mean(), mode='lines', name='SMA 20'))
            fig.update_layout(title=f'Candlestick chart for {ticker} with SMAs',
                              yaxis_title='Stock Price (USD/(Rupees)')
            st.plotly_chart(fig, use_container_width=True)
            
            fig_vol = go.Figure()
            fig_vol.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'))
            fig_vol.update_layout(title=f'Volume chart for {ticker}', yaxis_title='Volume')
            st.plotly_chart(fig_vol, use_container_width=True)
            
        else:
            st.write('No data found for the given parameters. Please check the ticker symbol and date range.')
    else:
        st.write('Please select both start and end dates.')

#stock news yfinance
def fetch_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    return news

st.sidebar.subheader("Fetch Stock News")
news_ticker = st.sidebar.text_input('Enter Stock Symbol for News:')

if st.sidebar.button('Get Stock News'):
    news = fetch_stock_news(news_ticker)
    if news:
        st.subheader(f'Stock News for {news_ticker}')
        for item in news:
            title = item.get('title', 'No title available')
            link = item.get('link', '#')
            time_published = item.get('provider_publish_time', 'No publish time available')
            st.write(f"**{title}**")
            st.write(f"{time_published}")
            st.write(f"[Read more]({link})")
            st.write("---")
    else:
        st.write('No news found for the given ticker.')








