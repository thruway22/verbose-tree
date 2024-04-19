import yfinance as yf
import streamlit as st
import pandas as pd

# Function to fetch data and calculate ratios
def fetch_data(tickers):
    data = yf.download(tickers, period="1d", group_by='ticker')
    results = []

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            market_cap = info.get('marketCap', None)
            book_value = info.get('bookValue', None)
            earnings = info.get('trailingEps', None)
            revenue = info.get('revenuePerShare', None)
            price = data[ticker].iloc[0]['Close'] if ticker in data.columns else None
            
            book_to_price = book_value / price if price and book_value else None
            earnings_to_price = earnings / price if price and earnings else None
            sales_to_price = revenue / price if price and revenue else None
            
            results.append({
                'Ticker': ticker
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
    
    # Reading tickers from a CSV file
    try:
        ticker_df = pd.read_csv('tickers.csv')
        tickers = ticker_df['ticker'].apply(lambda x: str(x) + ".SR").tolist()
        df = fetch_data(tickers)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Failed to read tickers from file: {e}")

if __name__ == "__main__":
    main()
