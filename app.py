import yfinance as yf
import streamlit as st
import pandas as pd

# Caching the data fetching to avoid repeated downloads
@st.cache
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

    try:
        ticker_df = pd.read_csv('tickers.csv')
        tickers = ticker_df['ticker'].tolist()
        df = fetch_data(tickers)

        # Checkbox to remove rows with None values
        remove_none = st.checkbox("Remove rows with any None values", False)
        if remove_none:
            df = df.dropna()

        # Slider to filter by market cap
        max_market_cap = st.number_input('Maximum Market Cap (Enter 0 for no limit)', min_value=0, value=0, step=1000000)
        if max_market_cap > 0:
            df = df[df['Market Cap'] <= max_market_cap]

        st.dataframe(df)
    except Exception as e:
        st.error(f"Failed to read tickers from file: {e}")

if __name__ == "__main__":
    main()
