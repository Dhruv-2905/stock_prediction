import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file,'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("images/ddd.jpg")

page_bg_img = f'''
<style>
[data-testid='stAppViewContainer']{{
background-image: url("data:image/png;base64,{img}"); 
background-size: cover;
}}
[data-testid='stHeader']{{
    background: rgba(0,0,0,0)
}}
[data-testid="stToolbar"]{{
    right: 2rem;
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(
        """
        <style>
            body {
                background-color: #2d3748;
            }
            h1, h2, h3, h4, h5, h6 {
                color: white;
            }
            .sidebar .sidebar-content {
                background-color: #1a202c;
                color: white;
            }
            .stButton>button {
                background-color: #4a5568;
                color: white;
                border-radius: 8px;
            }
            .highlight-box {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to fetch stock data
def fetch_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)
    return stock_data

# Function to preprocess data
def preprocess_data(data):
    data['Date'] = data.index
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    features = ['Year', 'Month', 'Day']
    target = 'Close'
    X = data[features]
    y = data[target]
    return X, y

# Function to train model
def train_model(X, y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# Function to predict stock prices
def predict_stock_prices(model, current_date):
    future_dates = pd.date_range(start=current_date, periods=90)  # Three months
    future_features = pd.DataFrame({
        'Year': future_dates.year,
        'Month': future_dates.month,
        'Day': future_dates.day
    })
    future_predictions = model.predict(future_features)
    return future_dates, future_predictions

# Function to fetch S&P 500 tickers
def fetch_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")[1:]  # Skip header row
    sp500_tickers = []
    for row in rows:
        ticker = row.find_all("td")[0].text.strip()
        sp500_tickers.append(ticker)
    return sp500_tickers

# Function to plot the results
def plot_results(data, future_dates, future_predictions, stock_symbol):
    plt.figure(figsize=(14, 7), facecolor='#f7fafc')
    plt.plot(data['Date'], data['Close'], label='Historical Close Prices', color='#2b6cb0', linewidth=2)
    plt.plot(future_dates, future_predictions, label='Predicted Close Prices', linestyle='--', color='#f56565', linewidth=2)
    plt.xlabel('Date', fontsize=12, color='#1a202c')
    plt.ylabel('Close Price', fontsize=12, color='#1a202c')
    plt.title(f'📈 Stock Price Prediction - {stock_symbol}', fontsize=14, color='black', pad=15)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#edf2f7')
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()
    # st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.pyplot(plt)
    st.markdown('</div>', unsafe_allow_html=True)

# Main function
def main():
    # st.title('📈 Stock Price Prediction')
    st.markdown(f'<h1 style="color: white;">📈 Stock Price Prediction</h1>', unsafe_allow_html=True)

    # Sidebar for selecting favorite stocks
    st.sidebar.title('Select Favorite Stocks')
    selected_favorites = st.sidebar.multiselect('Select stocks:', fetch_sp500_tickers())

    # Display selected stocks' graphs separately
    for selected_stock in selected_favorites:
        st.markdown(f'<h3 style="color: white;">{selected_stock}</h3>', unsafe_allow_html=True)
        current_date = datetime.datetime.now().date()
        start_date = current_date - datetime.timedelta(days=5*365)  # Last 5 years
        end_date = current_date

        # Fetch stock data for 5 years
        stock_data = fetch_stock_data(selected_stock, start_date, end_date)

        # Preprocess data
        X, y = preprocess_data(stock_data)

        # Train model
        model = train_model(X, y)

        # Predict stock prices for three months
        future_dates, future_predictions = predict_stock_prices(model, current_date)

        # Render the matplotlib graph
        plot_results(stock_data, future_dates, future_predictions, selected_stock)

if __name__ == "__main__":
    main()