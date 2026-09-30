# Frontier Agentic Trading System — Master Guide & Strategy Constitution

*Where this guide and any other document disagree, this master guide wins.*

## 1. System Overview & Mandate
The Frontier Agentic Trading System manages one Robinhood margin account ("Agentic", ••••5530, API id `865935530`, ~$50K equity) run as two sleeves:
1. **Frontier Equity Sleeve (~50% target):** A concentrated, unhedged frontier-tech equity book investing in deep tech / frontier growth themes (Space, Quantum, Nuclear, AI Biotech, Drones, Robotics, eVTOL, Autonomy, Rare Earths, Water, Semis/Memory).
2. **Cash-Secured-Put (CSP) Income Sleeve (~50% target):** An options income program generating repeatable cash premium to serve as the designated offset for Frontier equity drawdowns.

A second account ("Self-Managed", ••••1143, API id `5PY51143`) is read-only and inspected exclusively for wash-sale checks and informational cash. It is never traded and never transferred from.

A non-funded "Casino" section tracks speculative ideas for review and grading only. Nothing is ever traded from it.

---

## 2. Accounts, Allocation Bands & Authority

### 2.1 Account Roles & IDs
- **Agentic Account:** `865935530` (••••5530) — Limited margin, options level 3. Full autonomous execution within the rulebook: open, close, roll (within documented limits), cancel/replace, rebalance, sell covered calls. Holds all 20 Frontier Tech stocks. No per-trade confirmation required.
- **Self-Managed Account:** `5PY51143` (••••1143) — Read-only. Holds 4 Core stocks (CRWD, GLD, CGNX, DFTX) + 3 speculative calls (RPD, ONDS, HTZ). Inspected for wash-sale conflicts and informational cash sweep.

### 2.2 Allocation Bands
- **Target:** 50% Frontier Equity / 50% CSP Income.
- **Normal Operating Band:** 45% – 55%.
- **Hard Allocation Band:** 40% – 60%. Outside this band, no new risk may be added to the overweight sleeve until allocation is back inside the band.

### 2.3 Authority & Human Gates
The agent operates with full autonomous trading authority within this written rulebook.
**The only two human gates:**
1. A Torque short option intentionally crossing earnings or a binary event.
2. Any roll beyond the documented roll count (max 1 roll for Core puts, 0 for Torque, 1 for XSP, 1 for covered calls).

If human permission is unavailable, the agent must take the rule-compliant alternative (different expiration, skip, close, wait). It never improvises.

### 2.4 Fail-Closed Policy
Missing, stale, or contradictory hard-rule data removes all authority to add risk.
Risk-reducing closes still require exact position identification, fresh quotes, and limit orders.

---

## 3. Frontier Equity Sleeve Specification

### 3.1 Universe & Target Weights (Percent of Frontier Sleeve)
- **Anchors:**
  - `ASML` (~12%): EUV lithography monopoly. Exit if credible rival emerges, orders roll over multiple quarters, or trim above ~13%.
  - `RKLB` (~8%): #2 launcher with backlog, Neutron roadmap. Exit if Neutron slips/fails, Electron cadence drops, or burn without growth.
  - `CEG` (~7.5%): Largest US nuclear fleet powering hyperscalers. Exit if PPA momentum stalls, power prices collapse, or regulatory shift.
- **Growth:**
  - `IONQ` (~9%): Liquid quantum leader (trapped ion). Exit on roadmap slips, rival modality winning, or dilution spiral.
  - `RXRX` (~6%): AI drug discovery validated by Roche/Sanofi. Exit if pharma partnerships lapse or clinical failures repeat.
  - `TEM` (~5.5%): AI cancer diagnostics with revenue. Exit if revenue decelerates or reimbursement headwinds grow.
  - `ONDS` (~5%): Drone-warfare rollup, Army IDIQ. Exit if contracts fail to convert or dilution accelerates.
  - `ASTS` (~4.5%): Direct-to-cell satellite constellations. Exit on launch failures, carrier deal cancellation, or Starlink dominance.
  - `MP` (~3.5%): US rare-earth magnets. Exit on rare-earth price collapse or magnet ramp failure.
  - `INOD` (~3%): AI training-data infrastructure. Exit if revenue turns negative or customers in-source.
  - `MU` (~3%): HBM memory for AI accelerators. Exit if memory cycle rolls over or HBM share erodes.
- **Tail:**
  - `JOBY` (~3.5%): eVTOL certification leader. Exit if certification stalls, rival certifies first, or flight slips.
  - `AUR` (~3.5%): Autonomous trucking in Texas. Exit if safety incident halts ops or rollout stalls.
  - `QBTS` (~4%): Quantum-annealing lottery ticket. Exit if quantum deflates or annealing outpaced by gate-based.
  - `RGTI` (~3%): Superconducting quantum. Exit if theme deflates, falls behind rivals, or severe dilution.
- **ETFs (Breadth & Ballast):**
  - `ROBO` (~6%): Broad robotics (cap rather than grow).
  - `ARKG` (~4.5%): Gene-editing breadth.
  - `PHO` (~4%): Water infrastructure; uncorrelated holding.
  - `ARKX` (~2.5%): Space breadth beyond RKLB/ASTS.
- **Watch / Unclassified:**
  - `BETA`: Jake manual buy (~Sept 25), WATCH state pending diligence pass.

### 3.2 Thesis-State Framework
Every holding is categorized into one of three states on every run:
- **HEALTHY:** No exit criterion fired; milestones plausible. Adds, holds, and target raises allowed under sizing rules.
- **WATCH:** One material adverse fact, slipping milestone, or runway concern. **No automatic add.** Hold, trim, or rotate on evidence.
- **BROKEN:** Documented exit trigger verified, or severe generic failure (cancelled program, lost key customer, going-concern stress, regulatory block, or 2 WATCH conditions across 2 reporting periods). Execute exit. Price alone never creates BROKEN.

### 3.3 Position-Management Rules
1. **Drawdown is not exit:** 30–50% drop with intact thesis is an add candidate.
2. **Winner management (1.5× rule):** Trim only past 1.5× target weight. If thesis fundamentally improved, raise target. If reversible/sentiment move, trim back to 1.5× edge. Proceeds rotate to intact laggards.
3. **Taxes subordinate to risk:** Taxes decide between close discretionary moves, never override risk stops or broken exits.
4. **Dilution watch:** Track shares outstanding quarterly; distinguish filed ATM programs from actual issuance.
5. **No same-day round trips** in long-term holdings.
6. **Wash-sale check before every buy.**
7. **Covered calls on Frontier names:** WATCH-state only, never HEALTHY. Requires ≥100 settled shares, 15–20 delta, 31–45 DTE, strike ≥ broker cost basis, no dated catalyst before expiry, max 1 call per cycle, max 1 up-and-out roll.

### 3.4 Wash-Sale Discipline
- **Exclusion List (Floor, not ceiling):** Never hold NVDA, GEV, PLTR, CRWD, PANW, OKLO, CGNX. Never buy NLR, VTV, VOO, GLD, BND.
- **Absence rule:** A name missing from visible Robinhood pulls is not proof it isn't held elsewhere.
- **Cybersecurity ban:** Single names and ETFs banned from standing equity and CSPs (Core owns the sector).
- **Options cooldown:** 31-day freeze on any underlying closed at a loss.
- **XSP exemption:** Section 1256 index contracts are exempt from wash-sale rules.

---

## 4. Cash-Secured Put (CSP) Income Sleeve Specification

### 4.1 Core Role & Mechanics
The CSP sleeve generates repeatable cash income as a designated offset against equity drawdowns.
- **It is not a hedge:** Short puts are long beta and will lose in a broad crash.
- **Protection mechanism:** 15% rolling breaker, regime filter, and 20% hard cash reserve floor.
- **Assignment:** Treated as a paid limit order and an expected operating state into wheel inventory.

### 4.2 Sizing & Allocation at ~$50K Account
- Frontier Sleeve: 50% (~$25,000)
- CSP Sleeve: 50% (~$25,000)
- **Unencumbered Cash Reserve:** ≥20% hard floor (preferred working range 20–30%, target ~25% = $6,250).
- **Deployable Collateral:** ≤75% of CSP NAV (NORMAL regime).
- Sub-allocation of deployed collateral:
  - Core single-name CSPs: ~55% (~$10,300)
  - XSP defined-risk spreads: up to ~30% (aggregate max loss ≤10% of CSP NAV = ~$2,500)
  - Torque high-IV puts: ≤15% (~$2,800); 0% is an acceptable steady state.

### 4.3 Sleeve Accounting & Premium Lockbox
- `Frontier NAV` = Frontier positions + Frontier cash.
- `CSP NAV` = CSP cash (reserve + collateral) + wheel inventory market value − mark-to-market liability of open short options.
- `Account NAV` = Frontier NAV + CSP NAV (must reconcile to broker equity).
- `locked_open_premium` = Sum of opening credits of all open short options.
- `effective_free_cash` = broker free cash − `locked_open_premium`. Opening credits never fund new positions.

### 4.4 Contract Targets & Selection Gates
- **Core Puts:**
  - Delta: 16–25 (center ~20). DTE: 35–45.
  - Credit ≥1.4% of collateral per cycle (~12% annualized).
  - Bid/ask spread ≤8% of mid (prefer ≤5%).
  - Credit ≥3× bid/ask spread.
  - Open interest (OI) ≥50.
  - Roll destination exists: Next monthly cycle has OI ≥50 at same/lower strike.
  - No earnings or binary event before expiration.
- **XSP Bull Put Spreads:**
  - Short strike delta: 15–20. DTE: 35–45.
  - Width: $5–$10 (prefer $10). Net credit ≥8% of width.
  - Bid/ask spread ≤5% of mid. ≤9 contracts per order. Ladder across ≥2 expirations.
- **Torque Puts:**
  - Delta: 16–20. DTE: 35–45. Max 1 contract per name, max 1–2 names. Aggregate ≤15% of deployed collateral.
  - No earnings crossing without explicit human permission.

### 4.5 Regime Filter
Classified before every new short put:
- **NORMAL (VIX <22 & SPY ≥50DMA):** Standard rules; utilization up to 75% of CSP NAV.
- **ELEVATED (VIX 22–30, or SPY <50DMA but ≥200DMA):** Utilization ≤60%; prefer Core; Torque ≤7% of deployed.
- **STRESS (VIX 30–40, or SPY <200DMA):** No new Torque; no new puts in first STRESS session; then Core 10–16 delta, utilization ≤45%.
- **CRISIS (VIX >40, broad halt, or SPY −7% intraday):** No new short puts; risk reduction only.
*Conflicting signals always resolve to the more conservative regime.*

### 4.6 Concentration Limits & Circuit Breakers
- **Pacing:** Max 40% of remaining deployable collateral in any calendar week.
- **Per-Underlying Cap:** Max 25% of CSP NAV. **Combined hard cap: 20% of Agentic NAV after hypothetical assignment** (Frontier shares + wheel shares + strike value of open puts).
- **Per-Sector Cap:** Max 2 CSP underlyings per sector; CSP-only sector ≤35% of deployed collateral. **Combined hard cap: 35% of Agentic NAV after hypothetical assignment**.
- **XSP Governor:** Aggregate max loss ≤10% of CSP NAV.
- **Calendar-Month 6% Breaker:** CSP sleeve loss ≥6% of beginning-of-month CSP NAV → freeze new STO until next month.
- **Rolling-30-Day 15% Breaker:** Drawdown from 30-day peak CSP NAV ≥15% → freeze all new puts & Torque until drawdown <10% for 5 consecutive trading days.

### 4.7 Position Management & Exit Rules
- **Core Puts:**
  - Profit target: Buy-to-close at ≤50% of opening credit.
  - Loss handling: **No percentage stop. Accept assignment.** Close early only on BROKEN thesis, freefall gate (1-week drop worse than −12%), concentration/event failure, or CRISIS regime. A put at 3–4× credit with an intact thesis is HELD.
  - 21 DTE Checkpoint: Exactly 1 autonomous roll allowed per campaign if thesis is intact, no earnings before new expiry, 35–50 DTE, same/lower strike, delta ≤20, net credit. Otherwise close or hold to assignment.
- **Torque Puts:**
  - Profit target: Buy-to-close at ≤50% of credit.
  - Hard stop: Debit-to-close ≥3× credit → close immediately. Never roll through it.
  - Zero autonomous rolls.
- **XSP Spreads:**
  - Profit target: Buy-to-close at ≤50% of net credit.
  - Short strike breached after 21 DTE, or regime moves to STRESS/CRISIS → close. Before 21 DTE breach is held.
  - Max 1 roll: net credit, same/lower strike, 35–50 DTE.
  - **7 DTE Hard Rule: Close or roll without exception.**
- **Covered Calls (Wheel Inventory):**
  - Close at ~50% profit or reassess by 7 DTE.
  - Max 1 up-and-out roll per cycle if net credit and materially better outcome.
  - Strike selection: At or above cash-adjusted wheel basis. Follow below-basis recovery rules if stock is down >10%.

---

## 5. Execution State Machine & Kill Switches
Order state flow: `CANDIDATE → VALIDATED → PRE-FLIGHT → SUBMITTED → ACKNOWLEDGED → FILLED/CANCELED/REJECTED → RECONCILED`.

### Kill Switches (All New STO Prohibited When):
1. Reconciliation fails or broker state differs from internal state.
2. Unencumbered reserve would drop below 20% after trade and locked premium.
3. Either breaker (monthly 6% or rolling-30d 15%) is active.
4. Regime prohibits new risk.
5. Sleeve allocation band (40/60) or concentration cap (20% underlying, 35% sector) would be breached.
6. Quotes are stale or spread gate fails.
7. Earnings/event date status is unknown.
8. Unresolved assignment, corporate action, or order anomaly.
