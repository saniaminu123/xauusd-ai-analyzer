import os
import httpx
import pandas as pd
from dotenv import load_dotenv

from config import TIMEFRAMES, SYMBOLS, DEFAULT_CANDLES

load_dotenv()

BASE_URL = "https://api.twelvedata.com/time_series"

class TwelveDataError(RuntimeError):
    pass

async def get_candles(symbol: str, timeframe: str, outputsize: int = DEFAULT_CANDLES) -> pd.DataFrame:
    if symbol not in SYMBOLS:
        raise TwelveDataError("Unsupported symbol")
    if timeframe not in TIMEFRAMES:
        raise TwelveDataError("Unsupported timeframe")

    api_key = os.getenv("TWELVE_DATA_API_KEY")
    if not api_key:
        raise TwelveDataError("TWELVE_DATA_API_KEY is not configured")

    params = {
        "symbol": SYMBOLS[symbol]["provider"],
        "interval": TIMEFRAMES[timeframe],
        "outputsize": outputsize,
        "apikey": api_key,
        "format": "JSON",
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        payload = response.json()

    if payload.get("status") == "error":
        raise TwelveDataError(payload.get("message", "Market data error"))

    values = payload.get("values", [])
    if not values:
        raise TwelveDataError("No candle data returned")

    df = pd.DataFrame(values)
    df["datetime"] = pd.to_datetime(df["datetime"])
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"])
    return df.sort_values("datetime").reset_index(drop=True)
