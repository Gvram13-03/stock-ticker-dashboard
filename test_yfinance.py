import yfinance as yf
print("Testing yfinance...")
for symbol in ["MSFT", "AAPL", "GOOGL"]:
    ticker = yf.Ticker(symbol)
    for period in ["1d", "5d", "1mo"]:
        history = ticker.history(period=period)
        if not history.empty:
            print(f"Success for {symbol} ({period}): {history['Close'].iloc[-1]}")
            break
    else:
        print(f"No data for {symbol}")