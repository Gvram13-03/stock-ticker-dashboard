import yfinance as yf

def scrape_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1d")
    if not history.empty:
        return {"symbol": symbol, "price": history["Close"].iloc[-1]}
    return None

def test_scrape_stock_price():
    result = scrape_stock_price("MSFT")
    if result:
        assert result["symbol"] == "MSFT"
        assert result["price"] > 0
