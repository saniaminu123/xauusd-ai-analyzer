# SASI FX HUB PRO

Professional multi-market SMC/Fibonacci market-analysis application.

## Core workflow

**Market → Multi-Timeframe Structure → Liquidity → OB/FVG → Fibonacci → Interest Zone → IN ZONE → Confirmation → CONFIRMED → Trade Plan**

The application is deliberately designed **not to force an instant entry**.

### Status engine

- `WAIT` — price is outside the Interest Zone.
- `IN_ZONE` — price has entered the Interest Zone.
- `CONFIRMING` — confirmation conditions are being evaluated.
- `CONFIRMED` — configured confirmation conditions passed.
- `INVALID` — setup has been invalidated.

## Supported timeframes

1M, 5M, 15M, 30M, 1H, 4H, 1D

## Markets

XAUUSD, BTC/USD, ETH/USD, major forex pairs and indices can be configured through `backend/config.py`.

## Architecture

- Frontend: responsive HTML/CSS/JavaScript
- Backend: Python FastAPI
- Market data: Twelve Data adapter
- Analysis modules: structure, liquidity, FVG, order block, Fibonacci, interest zone, confirmation and risk
- API key: environment variable only; never commit secrets

## Run locally

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Put your Twelve Data API key in .env
uvicorn main:app --reload --port 8000
```

### 2. Frontend

Open `frontend/index.html`, or serve it:

```bash
cd frontend
python -m http.server 5500
```

Then open `http://localhost:5500`.

If the frontend is hosted separately, set `API_BASE` in `frontend/app.js`.

## Environment

`.env`:

```env
TWELVE_DATA_API_KEY=YOUR_KEY_HERE
```

Do not commit `.env`.

## Production notes

The supplied SMC calculations are a transparent prototype baseline. Before using live trading decisions, validate each detection rule against historical data and your broker's symbol/contract specifications. Confidence is a model score, not a probability of profit.

This project is an analysis/decision-support tool and does not guarantee trading results.
