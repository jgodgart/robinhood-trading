"""
sentiment_scoring.py — Deterministic Buy/Sell/Hold scoring + AGENTS.md rule overlay.

The composite score is a weighted blend of four factors, each normalized to [-2, +2]:
    news_thesis  (40%) — LLM read of news flow vs. our written thesis (search-grounded)
    technical    (25%) — trend (200DMA, 50/200 cross), 1-month momentum, overextension penalty
    analyst      (20%) — sell-side consensus (recommendationMean 1=Strong Buy … 5=Sell)
    target       (15%) — implied upside/downside to mean price target

Missing factors are dropped and the remaining weights renormalized. If fewer than two
factors are available the holding is UNRATED (fail-closed — never improvise a rating).

The SIGNAL (rating) is kept separate from the ACTION. The action is produced by the
rule overlay, which enforces the Constitution / AGENTS.md:
    - 1.5x Winner Trim Rule (+50% gain or >1.5x target weight) → harvest 20–25%
    - 30–50% drawdown with intact thesis → accumulation opportunity, never auto-stop
    - Price alone never breaks a thesis (Sell signal + intact thesis → HOLD/WATCH)
    - Account isolation: Self-Managed is read-only for the agent; Agentic adds are
      blocked for any ticker held in Self-Managed, on the wash-sale floor list, or in cooldown
"""

WEIGHTS = {"news_thesis": 0.40, "technical": 0.25, "analyst": 0.20, "target": 0.15}

# 1–5 display scale (composite + 3). Ordered low → high.
RATING_BANDS = [
    (-1.2, "STRONG SELL", "#D93025"),
    (-0.4, "SELL", "#F28B82"),
    (0.4, "HOLD", "#F9AB00"),
    (1.2, "BUY", "#81C995"),
    (99.0, "STRONG BUY", "#137333"),
]

WASH_SALE_FLOOR = {"NVDA", "GEV", "PLTR", "CRWD", "PANW", "OKLO", "CGNX", "NLR", "VTV", "VOO", "GLD", "BND"}
# 31-day loss cooldowns: ticker -> ISO date the cooldown ends (inclusive)
LOSS_COOLDOWNS = {"CELH": "2026-10-11"}

WINNER_TRIM_PCT = 50.0
DRAWDOWN_ACCUM_LOW = -50.0
DRAWDOWN_ACCUM_HIGH = -30.0


def _clamp(x, lo=-2.0, hi=2.0):
    return max(lo, min(hi, x))


def score_analyst(rec_mean, n_analysts):
    if not rec_mean or not n_analysts or n_analysts < 3:
        return None
    return round(_clamp(3.0 - float(rec_mean)), 2)


def score_target(upside_pct, n_analysts):
    if upside_pct is None or not n_analysts or n_analysts < 3:
        return None
    return round(_clamp(upside_pct / 15.0), 2)


def score_technical(price, dma50, dma200, ret_1m):
    if not price or not dma200:
        return None
    s = 1.0 if price > dma200 else -1.0
    if dma50:
        s += 0.5 if dma50 > dma200 else -0.5
    if ret_1m is not None:
        s += _clamp(ret_1m * 100 / 10.0, -1.0, 1.0)
    # Overextension: >20% above the 50DMA means chase risk / mean-reversion risk
    if dma50 and price > dma50 * 1.20:
        s -= 0.75
    elif dma50 and price < dma50 * 0.80:
        s += 0.25  # deeply oversold — partial offset, not a buy signal by itself
    return round(_clamp(s), 2)


def rating_for(composite):
    for upper, label, color in RATING_BANDS:
        if composite <= upper:
            return label, color
    return RATING_BANDS[-1][1], RATING_BANDS[-1][2]


def composite_score(factors):
    """factors: dict name -> score or None. Returns (composite or None, used_weights)."""
    avail = {k: v for k, v in factors.items() if v is not None and k in WEIGHTS}
    if len(avail) < 2:
        return None, {}
    wsum = sum(WEIGHTS[k] for k in avail)
    comp = sum(WEIGHTS[k] * v for k, v in avail.items()) / wsum
    return round(comp, 2), {k: round(WEIGHTS[k] / wsum, 3) for k in avail}


def _add_block_reason(ticker, account, self_managed_tickers, today_iso):
    if account != "agentic":
        return None
    if ticker in self_managed_tickers:
        return f"{ticker} is also held in Self-Managed (account isolation rule)"
    if ticker in WASH_SALE_FLOOR:
        return f"{ticker} is on the wash-sale floor exclusion list"
    end = LOSS_COOLDOWNS.get(ticker)
    if end and today_iso <= end:
        return f"{ticker} is in a 31-day loss cooldown through {end}"
    return None


def rule_overlay(h, rating, thesis_status, self_managed_tickers, today_iso, days_to_earnings=None):
    """
    h: holding context dict (ticker, account, kind, shares, pnl_pct, pct_portfolio, ...)
    Returns dict(action, action_color, rule, notes[list]).
    """
    ticker, account, kind = h["ticker"], h["account"], h.get("kind", "stock")
    notes = []
    if days_to_earnings is not None and 0 <= days_to_earnings <= 14:
        notes.append(f"Earnings in {days_to_earnings} days — expect a volatility event; avoid sizing up right before the print.")

    if rating is None:
        return {"action": "NO ACTION — UNRATED", "action_color": "#5F6368",
                "rule": "Fail-closed: insufficient live data to rate. No new risk until data reconciles.", "notes": notes}

    if kind == "option":
        side = h.get("option_side", "")
        if account == "agentic" and side == "short":
            rule = "Underlying signal only. The short put is governed by CSP rules: close at ≤50% credit; no % stop; close early only on BROKEN thesis, freefall gate (−12% in a week), or CRISIS regime."
            action = "MANAGE PER CSP RULES"
            if thesis_status == "BROKEN":
                action, rule = "CLOSE — THESIS BROKEN", "Thesis on the underlying is BROKEN → early close permitted under Core-put rules."
        else:
            action = "SIGNAL SUPPORTS CALL" if rating in ("BUY", "STRONG BUY") else (
                "SIGNAL UNDERMINES CALL" if rating in ("SELL", "STRONG SELL") else "SIGNAL NEUTRAL")
            rule = "Long call in Self-Managed (read-only for the agent). Underlying signal shown for Jake's manual decision; theta decay accelerates inside 30 DTE."
        return {"action": action, "action_color": _action_color(action), "rule": rule, "notes": notes}

    pnl_pct = h.get("pnl_pct", 0.0) or 0.0
    shares = h.get("shares", 0.0) or 0.0
    block = _add_block_reason(ticker, account, self_managed_tickers, today_iso)

    if thesis_status == "BROKEN":
        action, rule = "REDUCE / EXIT REVIEW", "Thesis is BROKEN on fundamentals (not price). Exit review triggered."
    elif pnl_pct >= WINNER_TRIM_PCT:
        lo, hi = shares * 0.20, shares * 0.25
        qty = f"{lo:.0f}–{hi:.0f} shares" if shares >= 8 else f"{lo:.2f}–{hi:.2f} shares"
        action = "HOLD CORE + TRIM 20–25%"
        rule = f"1.5× Winner Trim Rule: position is up {pnl_pct:+.0f}% (≥ +50%). Harvest {qty} to lock in principal; let the rest ride."
        if rating in ("SELL", "STRONG SELL"):
            action = "TRIM 25% NOW"
            rule += " Weak signal adds urgency — take the full 25%."
    elif DRAWDOWN_ACCUM_LOW <= pnl_pct <= DRAWDOWN_ACCUM_HIGH and thesis_status == "INTACT":
        action = "ACCUMULATE"
        rule = f"Drawdown rule: down {pnl_pct:.0f}% with thesis INTACT → accumulation opportunity, never an automatic stop."
    elif rating in ("BUY", "STRONG BUY"):
        action = "ADD ON WEAKNESS" if rating == "BUY" else "ADD"
        rule = "Signal and thesis aligned positive."
    elif rating == "HOLD":
        action, rule = "HOLD", "Mixed signals — no edge to add or trim."
    else:
        if thesis_status == "INTACT":
            action, rule = "HOLD — WATCH", "Weak signal, but price alone never breaks a thesis. Watch for fundamental confirmation."
        else:
            action, rule = "HOLD — NO ADDS", "Weak signal and thesis WEAKENING. Freeze adds; re-check next brief."

    if block and action.startswith(("ADD", "ACCUMULATE")):
        action = "HOLD (ADD BLOCKED)"
        rule += f" Add blocked: {block}."

    if account == "self_managed":
        notes.insert(0, "Self-Managed account is read-only for the agent — this is a recommendation for Jake to execute manually.")
        if ticker in WASH_SALE_FLOOR:
            notes.append(f"{ticker} is on the wash-sale floor list: trimming at a gain is fine; avoid selling at a loss and re-buying within 31 days.")
    if (h.get("pct_portfolio") or 0) >= 30:
        notes.append(f"Concentration: {ticker} is {h['pct_portfolio']:.0f}% of this account.")

    return {"action": action, "action_color": _action_color(action), "rule": rule, "notes": notes}


def _action_color(action):
    a = action.upper()
    if a.startswith(("REDUCE", "CLOSE", "TRIM 25", "SIGNAL UNDERMINES")):
        return "#D93025"
    if "TRIM" in a:
        return "#B06000"
    if a.startswith(("ADD", "ACCUMULATE", "SIGNAL SUPPORTS")):
        return "#137333"
    if a.startswith("NO ACTION"):
        return "#5F6368"
    return "#1967D2"
