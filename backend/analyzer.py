from dataclasses import dataclass, asdict
import math
import pandas as pd
import numpy as np

@dataclass
class Analysis:
    symbol: str
    timeframe: str
    price: float
    bias: str
    status: str
    confidence: int
    interest_low: float
    interest_high: float
    entry: float | None
    sl: float | None
    tp1: float | None
    tp2: float | None
    tp3: float | None
    rr: float | None
    reasons: list
    confirmations: dict
    structure: dict
    fibonacci: dict
    liquidity: dict
    order_block: dict
    fvg: dict

    def json(self):
        return asdict(self)

def _atr(df, n=14):
    prev = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev).abs(),
        (df["low"] - prev).abs()
    ], axis=1).max(axis=1)
    return float(tr.rolling(n).mean().iloc[-1]) if len(df) >= n else float((df["high"]-df["low"]).mean())

def _swings(df, lookback=3):
    highs, lows = [], []
    for i in range(lookback, len(df)-lookback):
        h = df["high"].iloc[i]
        l = df["low"].iloc[i]
        if h == df["high"].iloc[i-lookback:i+lookback+1].max():
            highs.append((i, float(h)))
        if l == df["low"].iloc[i-lookback:i+lookback+1].min():
            lows.append((i, float(l)))
    return highs, lows

def analyze(df: pd.DataFrame, symbol: str, timeframe: str) -> Analysis:
    price = float(df["close"].iloc[-1])
    atr = max(_atr(df), price * 0.0001)
    highs, lows = _swings(df)

    last_high = highs[-1][1] if highs else float(df["high"].iloc[-20:].max())
    prev_high = highs[-2][1] if len(highs) >= 2 else last_high
    last_low = lows[-1][1] if lows else float(df["low"].iloc[-20:].min())
    prev_low = lows[-2][1] if len(lows) >= 2 else last_low

    bullish = last_high >= prev_high and last_low >= prev_low
    bearish = last_high <= prev_high and last_low <= prev_low

    if bullish and not bearish:
        bias = "BULLISH"
    elif bearish and not bullish:
        bias = "BEARISH"
    else:
        bias = "NEUTRAL"

    # A transparent retracement zone based on the latest meaningful swing range.
    swing_high = max(last_high, price)
    swing_low = min(last_low, price)
    rng = max(swing_high - swing_low, atr * 2)

    if bias == "BULLISH":
        fib50 = swing_high - rng * 0.50
        fib618 = swing_high - rng * 0.618
        interest_low, interest_high = sorted([fib618, fib50])
        sl = interest_low - atr * 0.6
        entry = (interest_low + interest_high) / 2
        risk = max(entry - sl, atr * 0.5)
        tp1, tp2, tp3 = entry + risk*1.5, entry + risk*2.5, entry + risk*4
    elif bias == "BEARISH":
        fib50 = swing_low + rng * 0.50
        fib618 = swing_low + rng * 0.618
        interest_low, interest_high = sorted([fib50, fib618])
        sl = interest_high + atr * 0.6
        entry = (interest_low + interest_high) / 2
        risk = max(sl - entry, atr * 0.5)
        tp1, tp2, tp3 = entry - risk*1.5, entry - risk*2.5, entry - risk*4
    else:
        interest_low, interest_high = price-atr, price+atr
        entry = sl = tp1 = tp2 = tp3 = None
        risk = None

    in_zone = interest_low <= price <= interest_high if bias != "NEUTRAL" else False

    # Simple prototype confirmation checks.
    recent = df.iloc[-8:]
    swept_high = float(recent["high"].max()) > float(df["high"].iloc[-25:-8].max()) if len(df) > 25 else False
    swept_low = float(recent["low"].min()) < float(df["low"].iloc[-25:-8].min()) if len(df) > 25 else False

    bullish_mss = bias == "BULLISH" and price > float(df["high"].iloc[-5:-1].max())
    bearish_mss = bias == "BEARISH" and price < float(df["low"].iloc[-5:-1].min())
    mss = bullish_mss or bearish_mss

    # Basic FVG heuristic: last 3-candle imbalance.
    fvg = False
    if len(df) >= 3:
        a, b, c = df.iloc[-3], df.iloc[-2], df.iloc[-1]
        fvg = bool(c["low"] > a["high"] or c["high"] < a["low"])

    liquidity = swept_low if bias == "BULLISH" else swept_high if bias == "BEARISH" else False
    confirmation = {
        "higher_timeframe_alignment": bias != "NEUTRAL",
        "liquidity_sweep": bool(liquidity),
        "mss_or_choch": bool(mss),
        "fvg": bool(fvg),
        "interest_zone": bool(in_zone),
    }

    passed = sum(bool(v) for v in confirmation.values())
    confidence = min(95, 45 + passed * 10 + (5 if bias != "NEUTRAL" else 0))

    if bias == "NEUTRAL":
        status = "WAIT"
    elif not in_zone:
        status = "WAIT"
    elif mss and liquidity and fvg:
        status = "CONFIRMED"
    else:
        status = "IN_ZONE"

    reasons = []
    reasons.append(f"{bias.title()} structure" if bias != "NEUTRAL" else "Structure is mixed")
    reasons.append("Price is inside the Interest Zone" if in_zone else "Price is outside the Interest Zone")
    reasons.append("Liquidity sweep detected" if liquidity else "Liquidity confirmation pending")
    reasons.append("MSS/CHoCH detected" if mss else "MSS/CHoCH confirmation pending")
    reasons.append("FVG condition detected" if fvg else "FVG confirmation pending")

    rr = None
    if risk and entry:
        rr = round(abs(tp2-entry)/risk, 2)

    return Analysis(
        symbol=symbol, timeframe=timeframe, price=price, bias=bias, status=status,
        confidence=int(confidence), interest_low=float(interest_low), interest_high=float(interest_high),
        entry=float(entry) if entry else None, sl=float(sl) if sl else None,
        tp1=float(tp1) if tp1 else None, tp2=float(tp2) if tp2 else None, tp3=float(tp3) if tp3 else None,
        rr=rr, reasons=reasons, confirmations=confirmation,
        structure={"last_high": last_high, "last_low": last_low, "bias": bias},
        fibonacci={"50": float(fib50) if bias != "NEUTRAL" else None, "61.8": float(fib618) if bias != "NEUTRAL" else None},
        liquidity={"sweep_detected": bool(liquidity)},
        order_block={"status": "candidate"},
        fvg={"detected": bool(fvg)}
    )
