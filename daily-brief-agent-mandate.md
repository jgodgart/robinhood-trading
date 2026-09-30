# Daily Brief & Autonomous Agent Mandate

*Operating instructions for scheduled trading passes, trigger monitors, reconciliation, and automated execution.*

## 1. Operating Rhythm & Tasks
The agent runs four scheduled HTML reports and two intraday trigger monitors on trading days:

| Task | Cron (UTC) | Approx. ET | Scope | Output |
|---|---|---|---|---|
| **Pre-Market Report** | `30 12 * * *` | ~8:30am | Forward-looking full brief, thesis dashboard, candidate staging (STAGED — MARKET CLOSED). No option execution. Automatically emailed to jgodgart@gmail.com via `scripts/send_brief_email.py`. | `briefs/YYYY-MM-DD-premarket-brief.html` |
| **Market-Open Report** | `40 13 * * 1-5` | ~9:40am | Execution pass. Re-validate staged candidates with live quotes, execute valid CSPs/equity orders. | `briefs/YYYY-MM-DD-open-brief.html` |
| **Intraday Monitor (:30)** | `30 13-19 * * 1-5` | 9:30am–3:30pm | Silent trigger monitor for open options (50% profit, 3× stop, 21-DTE). No new STO. | Push notification on execution only |
| **Intraday Monitor (:00)** | `2 14-19 * * 1-5` | 10:02am–3:02pm | Alternate 30-min silent trigger monitor. | Push notification on execution only |
| **Closing Report** | `15 19 * * 1-5` | ~3:15pm | Risk management pass. Check all open positions before market close; execute required closes/rolls. | `briefs/YYYY-MM-DD-close-brief.html` |
| **Evening Report** | `0 0 * * *` | ~8:00pm | Backward-looking recap. Scoreboard, reflection, casino recap, tomorrow setup. | `briefs/YYYY-MM-DD-evening-brief.html` |

*Note: All crons are UTC. When Eastern Time shifts between EDT (UTC−4) and EST (UTC−5) in early November, crons must be reviewed.*

---

## 2. STEP 0: Mandatory Broker Reconciliation
Before evaluating trades, running scans, or writing reports, execute the following reconciliation:
1. `get_accounts`: Confirm authentication and identify both Agentic (`865935530`) and Core (`5PY51143`). If auth fails, STOP and alert immediately. Fail closed.
2. `get_equity_positions` (Agentic): Pull shares and split into Frontier holdings vs. Wheel inventory.
3. `get_option_positions` (Agentic, nonzero): Pull all open puts, covered calls, and spread legs.
4. `get_portfolio` (Agentic): Pull equity, cash, buying power, collateral.
5. `get_equity_orders` & `get_option_orders`: Retrieve all orders since last reconciliation cursor.
6. `get_equity_positions` & `get_portfolio` (Core): Verify exclusion list and informational cash.
7. Market regime check: VIX level, SPY vs. 50DMA and 200DMA.
8. Earnings / event calendar: Verify dates for every open option underlying and candidate.
9. Detect corporate actions, expirations, assignments, call-aways.
10. Rebuild sleeve accounting, lockbox (`locked_open_premium`), effective free cash, reserve %, and combined exposures.
11. Update `claude/account-snapshot.md` BEFORE generating any report.

---

## 3. STEP 0.5: Screener Pipeline
1. Check Account-State Gate: Reserve ≥20% after trade, regime limits, monthly/rolling breakers, weekly pacing ceiling.
2. Filter Exclusions: Core holdings (NVDA, GEV, PLTR, CRWD, PANW, OKLO, CGNX, etc.), Core ETFs (NLR, VTV, VOO, GLD, BND), active wash-sale clocks, 31-day loss cooldowns, cyber names, Frontier standing holdings.
3. Anti-Pattern / Quality Gate: No reverse splits in 36m, no deficiency notices, no going-concern warnings, dilution <15% TTM, no binary regulatory events before expiry.
4. Option Chain Pass: 35–45 DTE, 16–25 delta (Torque 16–20), spread ≤8% of mid, credit ≥1.4% of collateral, credit ≥3× spread, OI ≥50, roll destination verified.
5. Score candidates on 100-point framework.
6. Stage top 0–5 candidates in `claude/wheel-state.json`.

---

## 4. STEP 1: Automated Execution
- Limit orders only for all options.
- Calculate deterministic minimum credit / maximum debit guard from fresh bid/ask.
- Reprice only inside the guard; DAY time-in-force default.
- Idempotency ref_id on every order.
- Pre-flight check before submission: Re-verify reserve, regime, breakers, wash-sale list, quote spread.
- Partial fills are real positions; update state immediately.
- On fill: Append to `claude/agentic-ledger.jsonl`, update `claude/wheel-state.json`, and rebuild `claude/account-snapshot.md`.

---

## 5. Intraday Trigger Monitor Specifications
- Runs during options trading hours.
- Reconciles open options only.
- Checks:
  1. 50% profit target: Live debit-to-close ≤50% opening credit.
  2. Loss handling: Core puts accept assignment (no stop loss). Torque puts close if debit ≥3× credit. XSP spreads close if short strike breached after 21 DTE or if regime is STRESS/CRISIS; hard close/roll at 7 DTE.
  3. 21 DTE checkpoint: Core puts evaluate roll if thesis intact.
- If triggered: Execute limit order close/roll, append ledger, update wheel state, send alert.
- If no trigger: **Silence is expected.** Do not write files or send notifications.
