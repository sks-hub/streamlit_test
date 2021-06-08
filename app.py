import os

# from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import streamlit as st


# load_dotenv()
#API_KEY = str(os.environ.get("API_KEY"))
API_KEY = str(os.getenv("API_KEY"))

print("Value of 'API_KEY' environment variable :", API_KEY) 

# The st.cache decorator indicates that data will be downloaded only once and cached for future use.
@st.cache
def get_data(ticker):
    """Loads and caches data from the AlphaVantage API."""

    query = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY' \
    f'&outputsize=full&symbol={ticker}&apikey={API_KEY}&datatype=csv'

    df = pd.read_csv(query)
    if "Error" not in df.iloc[0][0]:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.set_index('timestamp')


def app():
    st.title("TDI Streamlit Milestone Project")
    st.markdown("""An interactive chart of stock closing prices using Streamlit
and Plot.ly. """)

    st.sidebar.title("Select plot parameters:")
    ticker = st.sidebar.text_input("Ticker (e.g. AAPL):")
    year = st.sidebar.selectbox("Year:", ["Select"] + list(range(2010, 2021)))
    month = st.sidebar.selectbox("Month:", ["Select", "January", "February",
                                            "March", "April", "May", "June",
                                            "July" ,"August", "September",
                                            "October", "November", "December"])

    # This keeps the app from running the plot until values are chosen
    if not (ticker and (year != "Select") and (month != "Select")):
        st.stop()

    df = get_data(ticker)
    if df is None:
        st.write(f"**Error: {ticker}** is not a valid ticker. Try another.")
        st.stop()

    df_plot = df.loc[f"{month} {year}"].reset_index()
    if len(df_plot) == 0:
        st.write(f"No data for {ticker} in {month} {year}. Try another date.")
        st.stop()

    fig = px.line(df_plot, x="timestamp", y="close",
                  title=f'{ticker}: {month} {year}')
    st.plotly_chart(fig)

if __name__ == "__main__":
    app()