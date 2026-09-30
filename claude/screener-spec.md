# Screener Specification (Config `2026-09-06a`)

## 1. Saved Robinhood Scans

| Scan Name | ID | Filters |
|---|---|---|
| **CSP Screening Engine** | `aa63bd34-b8dc-47b9-9163-847abc42b0f6` | STOCK/ETF; close $15–60; 30d avg vol ≥1.5M; chain OI ≥500; IV 25–50%; EPS >0; net margin >0; market cap ≥$2B; 1-week change ≥−12%; earnings date > target expiration + 7 days (**reset every run**) |
| **Frontier Emerging Names** | `1e3726b3-2d05-427a-8af4-f1ba733d680e` | STOCK; close ≥$5; cap $300M–$25B; 30d avg vol ≥500K; float ≥10M; frontier-adjacent sectors; 1-month change ≥+10%; above 50DMA |
| **Frontier Breakout Alerts** | `55c13d86-b418-4ef3-8daf-a3fd25e1523b` | Same universe; relative volume ≥2.0; day change ≥+5%; above 50DMA (closing and evening passes) |

*Note: XSP is not screened; it is a fixed-structure trade validated by the account-state gate, regime filter, and live chain pull.*

---

## 2. Options Funnel (Stage 1 to 5)

1. **Account-State Gate:**
   - Reserve ≥20% after hypothetical trade
   - Collateral utilization below regime cap (75% Normal, 60% Elevated, 45% Stress, 0% Crisis)
   - Both circuit breakers inactive (Monthly 6%, Rolling-30d 15%)
   - Weekly pacing ceiling (<40% of remaining deployable capital deployed this calendar week)
   - Expiration cluster assignment capacity confirmed

2. **Exclusion Join:**
   - Core holdings & ETFs (NVDA, GEV, PLTR, CRWD, PANW, OKLO, CGNX, NLR, VTV, VOO, GLD, BND)
   - Active wash-sale clocks & 31-day loss cooldowns
   - Standing Frontier equity holdings
   - Cybersecurity single names and ETFs
   - December tax harvest watch list

3. **Anti-Pattern & Fundamental Quality Gate:**
   - No reverse split in last 36 months
   - No exchange deficiency or listing notice
   - No going-concern warning in filings
   - Dilution watch: TTM shares outstanding increase <15%
   - No pending M&A or binary regulatory/clinical date before expiration
   - Put-volume spike check & accounting flags

4. **Options Chain Pass:**
   - 35–45 DTE
   - Delta: Core 16–25 (center ~20), Torque 16–20
   - Bid/ask spread ≤8% of mid (prefer ≤5%)
   - Open interest ≥50 per contract
   - Minimum credit: ≥1.4% of collateral per cycle (~12% annualized)
   - Spread ratio: Credit ≥3× bid/ask spread
   - Roll destination: Next monthly cycle exists with OI ≥50 at same/lower strike

5. **100-Point Scoring Framework:**
   - **Cash-income efficiency (35%):** Credit as % of collateral annualized
   - **Volatility Risk Premium (VRP) evidence (15%):** IV − HV from scan columns
   - **Downside cushion (10%):** Strike distance from spot
   - **Execution quality (10%):** Tightness of bid/ask spread & contract liquidity
   - **Business / assignment quality (10%):** Profitability, balance sheet strength, durable franchise
   - **Diversification / correlation vs Frontier (10%):** Low beta to tech/growth holdings
   - **Wheel optionality (5%):** Attractive covered call candidate if assigned
   - **Regime / technical fit (5%):** Moving average trend and support alignment

*Stage 5 Candidate Record must include all 27 required audit fields before submission to executor.*
