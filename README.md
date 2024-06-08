# Stock Price Prediction

A Streamlit application for predicting stock prices using historical data. This application leverages the Yahoo Finance API, Random Forest Regressor for machine learning, and Plotly for data visualization. The app also features a background image and custom styles.

## Features

- Fetch historical stock data from Yahoo Finance.
- Preprocess stock data for machine learning.
- Train a Random Forest Regressor model to predict future stock prices.
- Visualize actual vs. predicted stock prices using Plotly.
- Fetch and display S&P 500 tickers.
- Custom background and styles using CSS.

## Requirements

- Python 3.x
- Streamlit
- pandas
- yfinance
- scikit-learn
- plotly
- requests
- beautifulsoup4
- streamlit-extras
- base64

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Dhruv-2905/stock.git
    cd stock
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Add a background image `ddd.jpg` to the project directory.

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Select your favorite S&P 500 stocks from the sidebar and view the predictions.

## Project Structure

│
├── app.py # Main Streamlit application script
├── requirements.txt # List of dependencies
├── ddd.jpg # Background image file
├── README.md # Project documentation


## Code Overview

### `app.py`

- **Imports**: Imports necessary libraries and modules.
- **Background Image Setup**: Loads and sets a background image for the app.
- **Fetch Stock Data**: Fetches historical stock data using Yahoo Finance API.
- **Preprocess Data**: Preprocesses the stock data for training the machine learning model.
- **Train Model**: Trains a Random Forest Regressor model.
- **Predict Stock Prices**: Predicts future stock prices for the next month.
- **Fetch S&P 500 Tickers**: Fetches the list of S&P 500 companies from Wikipedia.
- **Main Function**: The main function that sets up the Streamlit interface, fetches data, trains the model, and displays the results.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

