import os
import sys
# from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import streamlit as st
import requests

# load_dotenv()
API_KEY = str(os.environ.get("API_KEY"))

print("Value of 'API_KEY' environment variable :", API_KEY) 


progress_bar = st.sidebar.progress(0)

# The st.cache decorator indicates that data will be downloaded only once and cached for future use.
@st.cache
def load_data(ticker):
    """Returns pandas dataframe after loading the data from Alphavantage

    Parameters
    ----------
    ticker : str
        The name of the ticker, like 'AAPL'
    
    Returns
    -------
    df(dataframe)
        pandas dataframe having the ticker stock information 
    """

    API_URL = "https://www.alphavantage.co/query"
    print("Retrieving stock price data from Alpha Vantage ...")
    
    params = { 
        "function": "TIME_SERIES_DAILY", 
        "symbol": ticker,
        "outputsize" : "full",
        "datatype": "csv", 
        "apikey": API_KEY 
        } 
    
    response = requests.get(API_URL, params=params)
    print("Data has been successfully downloaded...")
    # sys.stdout.flush()
    
    # Check if the response is ok (200) or "Error Message": "Invalid API call in the response text
    if response.status_code == 200 and not "Error" in response.text:

        data = [row.strip().split(',') for row in response.text.split('\n')]
        df = pd.DataFrame(data[1:-1], columns=data[0])

        # Convert the timestamp to datetime and set it as index
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.set_index('timestamp')
    
    return None

def main():

    st.title("TDI milestone project(streamlit)")
    st.markdown("""An interactive chart of stock closing prices using Streamlit and Plot.ly. """)
    st.sidebar.title("Select plot parameters:")
    
    ticker = st.sidebar.text_input("Stock Ticker (e.g. AAPL):")
    year = st.sidebar.slider('Year:', min_value=2010, max_value=2021,step=1)
    month = st.sidebar.selectbox("Month:", ["Select", "January", "February","March", "April", "May", "June","July" ,"August", "September","October", "November", "December"])
    
    # if year and month not selected and no ticker is entered
    if not ((year != "Select") and (month != "Select") and ticker):
        st.stop()

    # Load data
    df = load_data(ticker)
    
    # if no data found for the stock ticker
    if df is None:
        st.error(f"{ticker} is not a valid ticker. Try another.")
        st.stop()

    plot_data = df.loc[f"{month} {year}"].reset_index()

    # if there is no data for the ticker for the month and year selected.
    if len(plot_data) == 0:
        st.write(f"No data for {ticker} in {month} {year}. Try another date.")
        st.stop()

    # Plot the figure
    fig = px.line(plot_data, x="timestamp", y="close", title=f'{ticker}: {month} {year}')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()