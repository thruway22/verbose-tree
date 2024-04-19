import yfinance as yf
import streamlit as st
import pandas as pd

# Function to fetch data and calculate ratios
def fetch_data(tickers):
    data = yf.download(tickers, period="1y", group_by='ticker')
    results = []

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            market_cap = info['marketCap']
            book_value = info['bookValue']
            earnings = info['trailingEps']
            revenue = info['revenuePerShare']
            price = data[ticker].iloc[0]['Close']
            
            book_to_price = book_value / price if price else None
            earnings_to_price = earnings / price if price else None
            sales_to_price = revenue / price if price else None
            
            results.append({
                'Ticker': ticker,
                'Market Cap': market_cap,
                'Book Value-to-Price Ratio': book_to_price,
                'Earnings-to-Price Ratio': earnings_to_price,
                'Sales-to-Price Ratio': sales_to_price
            })
        except Exception as e:
            st.error(f"Error processing {ticker}: {e}")
    
    return pd.DataFrame(results)

# Streamlit app
def main():
    st.title('Saudi Stock Financial Ratios')
    tickers = st.text_input('Enter ticker symbols separated by space (e.g., "2222.SR 1150.SR")')
    if tickers:
        ticker_list = tickers.split()
        df = fetch_data(ticker_list)
        st.dataframe(df)

if __name__ == "__main__":
    main()
