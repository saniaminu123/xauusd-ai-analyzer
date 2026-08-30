from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from config import SYMBOLS, TIMEFRAMES
from data_provider import get_candles, TwelveDataError
from analyzer import analyze

app = FastAPI(title="SASI FX HUB PRO API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"ok": True, "service": "SASI FX HUB PRO"}

@app.get("/api/symbols")
async def symbols():
    return {"symbols": SYMBOLS, "timeframes": list(TIMEFRAMES.keys())}

@app.get("/api/analysis/{symbol}")
async def analysis(symbol: str, timeframe: str = Query("1M")):
    symbol = symbol.upper()
    timeframe = timeframe.upper()
    try:
        df = await get_candles(symbol, timeframe)
        result = analyze(df, symbol, timeframe)
        return result.json()
    except TwelveDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")
