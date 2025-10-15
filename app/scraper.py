import yfinance as yf
from sqlalchemy.orm import Session
from .models import StockPrice
from datetime import datetime

def scrape_stock_price(symbol: str, db: Session):
    try:
        ticker = yf.Ticker(symbol)
        for period in ["1d", "5d", "1mo"]:
            history = ticker.history(period=period)
            if not history.empty:
                price = history["Close"].iloc[-1]
                print(f"Success for {symbol} ({period}): {price}")
                db_stock = StockPrice(symbol=symbol, price=price, timestamp=datetime.utcnow())
                db.add(db_stock)
                db.commit()
                db.refresh(db_stock)
                return db_stock
        print(f"No data found for {symbol} across periods")
        return None
    except Exception as e:
        print(f"Error scraping {symbol}: {e}")
        return None