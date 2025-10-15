from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
from . import database, models, scraper, streaming
from .database import get_db
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

scheduler = BackgroundScheduler()
def scheduled_scrape():
    for symbol in ["MSFT", "GOOGL", "AAPL"]:  # Try multiple
        price_data = scraper.scrape_stock_price(symbol, next(get_db()))
        if price_data:
            streaming.manager.broadcast({
                "symbol": symbol,
                "price": price_data.price,
                "timestamp": str(price_data.timestamp)
            })
            break
        else:
            streaming.manager.broadcast({
                "symbol": symbol,
                "price": None,
                "timestamp": str(datetime.utcnow()),
                "message": f"No data for {symbol}"
            })

scheduler.add_job(scheduled_scrape, "interval", seconds=60)  # Longer interval
scheduler.start()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Stock Ticker Dashboard API"}

@app.get("/prices/{symbol}")
def get_prices(symbol: str, db: Session = Depends(get_db)):
    return db.query(models.StockPrice).filter(models.StockPrice.symbol == symbol).all()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, symbol: str = "MSFT"):
    await streaming.manager.connect(websocket)
    try:
        while True:
            price_data = scraper.scrape_stock_price(symbol, next(get_db()))
            if price_data:
                await streaming.manager.broadcast({
                    "symbol": symbol,
                    "price": price_data.price,
                    "timestamp": str(price_data.timestamp)
                })
            else:
                await streaming.manager.broadcast({
                    "symbol": symbol,
                    "price": None,
                    "timestamp": str(datetime.utcnow()),
                    "message": f"No data for {symbol}"
                })
            await websocket.receive_text()
    except:
        streaming.manager.disconnect(websocket)