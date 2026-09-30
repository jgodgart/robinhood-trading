# Book Principles & Literature Mapping (Sept 6)

The strategy incorporates principles from foundational options, risk management, and quantitative trading literature:

| Author / Text | Principle | Implementation Status | Implementation Details |
|---|---|---|---|
| **Sebastian** (*Option Volatility & Pricing*) | Monthly 6% Loss Breaker | **EMBEDDED** | Hard freeze on new sell-to-open if month-to-date CSP loss ≥6% of month-start NAV. |
| **Sebastian** | Credit ≥3× Spread | **EMBEDDED** | Hard entry gate: Prevents crossing wide markets that erode edge. |
| **Taleb / Bittman** | Stress Testing (-10% / -20% Spot + 50% IV) | **EMBEDDED** | Required calculation in every pre-market brief repricing live short options. |
| **Lowenstein** (*When Genius Failed*) | Combined Aggregate Delta | **EMBEDDED** | Sum of short-put delta + beta-adjusted Frontier equity delta reported as a single leverage metric. |
| **Warner** | No VIX Option Hedges | **EMBEDDED** | VIX options decay rapidly; hedges, if ever authorized, must be defined-risk SPX/XSP puts. |
| **McMillan** (*Options as a Strategic Investment*) | Roll Destination Check | **EMBEDDED** | An option cannot be opened unless the next monthly cycle has ≥50 OI at same/lower strike. |
| **McMillan** | 90th Percentile IV Gate | **NOT ADOPTED** | Too restrictive in low-vol regimes; VRP (IV - HV) used instead. |
| **Sebastian** | 2% Single-Name Trade Cap | **NOT ADOPTED** | Impractical for a $50K account trading quality names ($15–$60 stocks require $1.5K–$6K collateral). 20% underlying cap used. |
| **Sinclair** (*Volatility Trading*) | Earnings Volatility Arbitrage | **NOT ADOPTED** | Earnings crossing is banned for Core and restricted for Torque to protect capital from jump risk. |
| **Chan** (*Algorithmic Trading*) | Z-Score Pullback Entries | **CONTEXT** | Used as an optional secondary context signal rather than a rigid entry gate. |
