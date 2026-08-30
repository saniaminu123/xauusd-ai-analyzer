from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from pathlib import Path

out = Path("/mnt/data/SASI_FX_HUB_PRO_Full_App_Specification.docx")

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.55)
sec.bottom_margin = Inches(0.55)
sec.left_margin = Inches(0.65)
sec.right_margin = Inches(0.65)

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("SASI FX HUB PRO")
r.bold = True
r.font.size = Pt(24)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("FULL PROFESSIONAL APP SPECIFICATION — v2.0")
r.bold = True
r.font.size = Pt(13)

doc.add_paragraph(
    "Purpose: turn the current XAUUSD SMC analyzer into a professional multi-market trading-analysis "
    "platform that identifies Interest Zones first and only unlocks an entry after the required confirmation."
)

def h(text, level=1):
    doc.add_heading(text, level=level)

def bullets(items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")

def nums(items):
    for item in items:
        doc.add_paragraph(item, style="List Number")

h("1. Core Product Concept")
doc.add_paragraph(
    "SASI FX HUB PRO must not behave like an instant signal generator. Its main workflow is: "
    "Market → Trend → Liquidity → POI → Interest Zone → Price enters zone → Confirmation → Entry → "
    "Risk/Targets → Management → Invalidation."
)
bullets([
    "Primary objective: identify high-confluence areas rather than chase current price.",
    "No BUY/SELL confirmation while price is outside the Interest Zone.",
    "Show WAIT when the market is not ready.",
    "Show IN ZONE when price reaches the calculated area.",
    "Show CONFIRMED only when the selected confirmation rules are satisfied.",
    "Show INVALID when the setup is structurally broken.",
    "Every setup must display the reasons behind its score."
])

h("2. Supported Markets")
bullets([
    "Metals: XAUUSD and other supported metals.",
    "Crypto: BTC/USD, ETH/USD and other supported crypto symbols.",
    "Forex: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD and additional supported pairs.",
    "Indices: NAS100, US30, SPX500 and additional supported indices.",
    "Use a symbol configuration layer so new instruments can be added without rewriting the analyzer."
])

h("3. Timeframes")
bullets([
    "1M — execution / scalping confirmation.",
    "5M — setup and POI refinement.",
    "15M — intraday structure.",
    "30M — structure/context.",
    "1H — higher-timeframe bias.",
    "4H — major structure.",
    "1D — daily directional context.",
    "Recommended automatic multi-timeframe stack for scalping: 1H → 15M → 5M → 1M.",
    "Allow the user to choose a single timeframe or enable Multi-Timeframe mode."
])

h("4. Professional Navigation")
bullets([
    "Dashboard",
    "Market Scanner",
    "Chart & Analysis",
    "Trade Plan",
    "Alerts",
    "Backtest",
    "Watchlist",
    "News / Market Events",
    "Settings",
    "Profile / Pro subscription"
])

h("5. Dashboard")
bullets([
    "Live market status.",
    "Favorite symbols.",
    "Top setups ranked by confluence score.",
    "Interest Zones currently being approached.",
    "Setups currently IN ZONE.",
    "Confirmed setups.",
    "Invalidated setups.",
    "Daily analysis summary.",
    "Compact risk dashboard."
])

h("6. Market Scanner")
doc.add_paragraph("Each row should contain:")
bullets([
    "Symbol and market name.",
    "Direction: BULLISH / BEARISH / NEUTRAL.",
    "Interest Zone high and low.",
    "Distance from current price to zone.",
    "Status: WAIT / IN ZONE / CONFIRMED / INVALID.",
    "Confidence / Confluence score.",
    "Timeframe alignment.",
    "Favorite/star button.",
    "Tap row to open full analysis."
])

h("7. Chart & Analysis Engine")
bullets([
    "Professional candlestick chart.",
    "Zoom and pan.",
    "1M through 1D timeframe controls.",
    "Multi-timeframe badge.",
    "Current price line.",
    "Interest Zone rectangle.",
    "Order Blocks.",
    "Fair Value Gaps.",
    "Liquidity pools and previous highs/lows.",
    "Equal highs / equal lows.",
    "BOS labels.",
    "CHoCH / MSS labels.",
    "Fibonacci retracement with configurable levels.",
    "Entry, SL and TP markers after a valid setup is calculated.",
    "Optional visibility switches for each SMC layer."
])

h("8. Interest Zone Logic")
doc.add_paragraph("The most important product change is the Interest-Zone-first workflow.")
nums([
    "Determine higher-timeframe directional bias.",
    "Detect meaningful swing high/low structure.",
    "Detect liquidity pools and recent liquidity events.",
    "Locate candidate Order Blocks and FVGs.",
    "Calculate Fibonacci retracement where applicable.",
    "Score overlap/confluence between POIs.",
    "Create a zone with upper and lower boundaries.",
    "Keep trade status at WAIT while price is outside the zone.",
    "Change to IN ZONE when live price enters the boundaries.",
    "Require the configured confirmation trigger before CONFIRMED.",
    "Calculate entry trigger, invalidation, stop and targets.",
    "Invalidate if the structural condition or invalidation price is broken."
])

h("9. Confirmation Rules")
bullets([
    "Liquidity sweep can be required before confirmation.",
    "Bullish/bearish MSS or CHoCH can be required.",
    "FVG reaction can be required.",
    "Order Block reaction can be required.",
    "Higher-timeframe bias must be aligned unless the user enables counter-trend setups.",
    "The app must clearly show which conditions are PASS / WAIT / FAIL.",
    "Do not label a setup CONFIRMED merely because price touched the Interest Zone."
])

h("10. Trade Plan")
bullets([
    "Direction: BUY or SELL.",
    "Interest Zone: exact high/low.",
    "Entry: exact trigger price or 'TBD — confirmation required'.",
    "Stop Loss.",
    "TP1, TP2 and TP3.",
    "Risk in price points/pips.",
    "Reward to each target.",
    "R:R ratio.",
    "Confidence/confluence score.",
    "Invalidation condition.",
    "Reason for waiting.",
    "Next action.",
    "Set Alert for Zone button."
])

h("11. Example — XAUUSD BUY")
bullets([
    "Bias: BULLISH.",
    "Interest Zone: 4,590–4,598.",
    "Current price: 4,605.",
    "Status: WAIT.",
    "Rule: wait for price to enter 4,590–4,598.",
    "After entering zone: wait for bullish MSS/CHoCH plus FVG/OB reaction.",
    "Only then unlock BUY CONFIRMED.",
    "Illustrative SL: below structural invalidation.",
    "Illustrative targets: TP1 / TP2 / TP3.",
    "The numbers must be calculated from live market structure in production; prototype numbers are examples only."
])

h("12. Confluence Score")
bullets([
    "Trend alignment.",
    "Higher-timeframe structure.",
    "Liquidity event.",
    "Order Block quality.",
    "FVG quality.",
    "Fibonacci alignment.",
    "MSS/CHoCH confirmation.",
    "Distance to invalidation.",
    "Risk/reward quality.",
    "Session/market-condition filter.",
    "Display both the total score and a breakdown so the user understands why the score exists."
])

h("13. Alerts")
bullets([
    "Price approaching Interest Zone.",
    "Price entered Interest Zone.",
    "Confirmation detected.",
    "Setup invalidated.",
    "TP1 reached.",
    "TP2 reached.",
    "TP3 reached.",
    "Optional push/browser notifications.",
    "Per-symbol and per-timeframe alert settings.",
    "Cooldown to prevent repeated alerts."
])

h("14. Risk Management Module")
bullets([
    "User enters account balance.",
    "Optional risk-per-trade percentage.",
    "Calculate position size from SL distance and instrument contract specifications.",
    "Display estimated monetary risk.",
    "Display potential reward.",
    "Never present calculated lot size as a guarantee of broker execution.",
    "Include a manual-risk override.",
    "Optional daily loss limit and maximum number of active setups."
])

h("15. Backtest / Replay")
bullets([
    "Select symbol and timeframe.",
    "Choose historical date range.",
    "Replay candles.",
    "Generate Interest Zones using the same production rules.",
    "Record WAIT → IN ZONE → CONFIRMED → INVALID.",
    "Track win rate, average R:R, expectancy, maximum drawdown and number of setups.",
    "Separate backtest results from live signals."
])

h("16. Data & Python Architecture")
bullets([
    "Frontend: responsive web app / PWA.",
    "Backend: Python service for market-data processing and SMC analysis.",
    "Market data adapter: Twelve Data or another supported provider.",
    "API key must remain server-side in production; do not expose private provider keys in browser JavaScript.",
    "Use a WebSocket or polling layer for live price updates depending on provider capability.",
    "Cache candles to reduce unnecessary API calls.",
    "Normalize symbols because broker/provider symbol names can differ.",
    "Store configuration and analysis results in a database or lightweight persistence layer.",
    "Expose clean API endpoints such as /markets, /candles, /analysis, /alerts and /settings."
])

h("17. Suggested Python Components")
bullets([
    "data_provider.py — live and historical market data.",
    "symbol_config.py — instrument specifications and symbol mapping.",
    "timeframes.py — 1M to 1D mappings.",
    "market_structure.py — swings, BOS and CHoCH/MSS.",
    "liquidity.py — EQH/EQL, previous highs/lows and sweeps.",
    "order_blocks.py — OB detection and validation.",
    "fvg.py — Fair Value Gap detection.",
    "fibonacci.py — retracement and zone calculations.",
    "interest_zone.py — POI merging and zone scoring.",
    "confirmation.py — confirmation state machine.",
    "risk.py — SL, targets and position-size calculations.",
    "alerts.py — zone/confirmation/invalidation notifications.",
    "backtest.py — historical replay and performance metrics.",
    "api.py — frontend/backend endpoints."
])

h("18. State Machine")
doc.add_paragraph("Use a strict state machine:")
bullets([
    "WAIT — no zone touch.",
    "IN_ZONE — price is inside zone; entry is still locked.",
    "CONFIRMING — confirmation conditions are being evaluated.",
    "CONFIRMED — all required conditions passed.",
    "INVALID — setup no longer valid.",
    "COMPLETED — target reached or trade manually closed."
])

h("19. Settings")
bullets([
    "Default market.",
    "Default timeframe.",
    "Multi-timeframe stack.",
    "Fibonacci levels.",
    "Minimum confluence score.",
    "Required confirmation conditions.",
    "Zone width tolerance.",
    "Session filter.",
    "Risk settings.",
    "Alert settings.",
    "Chart visibility settings.",
    "Theme and display preferences."
])

h("20. Professional UI Requirements")
bullets([
    "Dark professional trading-terminal appearance.",
    "Gold SASI branding.",
    "Responsive desktop/tablet/mobile layout.",
    "Fast-loading dashboard.",
    "Clear status colors: WAIT, IN ZONE, CONFIRMED, INVALID.",
    "No clutter: advanced SMC layers can be toggled.",
    "Large touch targets for iPhone.",
    "Persistent navigation on desktop and bottom navigation on mobile.",
    "Clear separation between analysis and execution."
])

h("21. Security")
bullets([
    "Never put private API keys into public frontend source code.",
    "Use HTTPS in production.",
    "Authenticate user accounts.",
    "Rate-limit analysis endpoints.",
    "Validate all market-data inputs.",
    "Log errors without exposing secrets.",
    "Store user API keys encrypted if the product ever allows users to supply their own keys."
])

h("22. Production Roadmap")
nums([
    "Build the new frontend from the approved design.",
    "Connect Python backend.",
    "Connect live market-data provider.",
    "Implement candle normalization for all instruments.",
    "Implement SMC detection modules.",
    "Implement Interest Zone and confirmation state machine.",
    "Connect live chart.",
    "Implement scanner.",
    "Implement alerts.",
    "Implement risk module.",
    "Add backtesting.",
    "Test against historical charts.",
    "Deploy backend and frontend.",
    "Add authentication and Pro subscription if required."
])

h("23. Important Trading-Logic Disclaimer")
doc.add_paragraph(
    "SASI FX HUB PRO should be presented as an analysis and decision-support tool, not as a guaranteed-profit "
    "signal system. Confidence scores are model scores, not probabilities of profit. Live prices, spreads, "
    "slippage, liquidity and execution can differ from the analysis."
)

h("24. Final Product Definition")
doc.add_paragraph(
    "The finished SASI FX HUB PRO should feel like a professional trading terminal: the user selects a market, "
    "chooses 1M–1D or Multi-Timeframe analysis, sees structure and SMC evidence, receives a clearly defined "
    "Interest Zone, waits for price to reach it, receives confirmation only when the rules pass, and then gets "
    "a complete Trade Plan with invalidation, targets, R:R and alerts."
)

doc.save(out)
print(out)

