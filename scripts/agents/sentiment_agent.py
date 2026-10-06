"""
sentiment_agent.py — Buy/Sell/Hold sentiment engine for every holding in both accounts.

For each holding:
  1. Quant layer (yfinance): analyst consensus, price targets, trend/momentum, valuation,
     next earnings date, recent headlines.
  2. Thesis layer (Gemini + Google Search grounding): what is actually going on with the
     company, what SUPPORTS our thesis, what REFUTES it, thesis status, and a news score.
  3. Scoring + rule overlay (sentiment_scoring.py): composite 1–5 rating and a
     rule-compliant action (trim / add / hold / accumulate / blocked).

Fail-closed: if the quant layer is missing the holding is UNRATED. If the LLM layer fails
the rating falls back to quant-only and is flagged as such — never fabricated.
"""
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime

import yfinance as yf

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.config import GEMINI_MODEL
from agents import sentiment_scoring as sc

BANNED_PHRASES = [re.compile(r"in plain english:?", re.I)]


def _clean(text):
    if not isinstance(text, str):
        return text
    for p in BANNED_PHRASES:
        text = p.sub("", text)
    return text.strip()


def fetch_quant(ticker):
    t = yf.Ticker(ticker)
    info = t.info or {}
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    q = {
        "price": price,
        "target_mean": info.get("targetMeanPrice"),
        "target_low": info.get("targetLowPrice"),
        "target_high": info.get("targetHighPrice"),
        "rec_mean": info.get("recommendationMean"),
        "rec_key": info.get("recommendationKey"),
        "n_analysts": info.get("numberOfAnalystOpinions"),
        "high_52w": info.get("fiftyTwoWeekHigh"),
        "low_52w": info.get("fiftyTwoWeekLow"),
        "dma50": info.get("fiftyDayAverage"),
        "dma200": info.get("twoHundredDayAverage"),
        "forward_pe": info.get("forwardPE"),
        "ps_ttm": info.get("priceToSalesTrailing12Months"),
        "revenue_growth": info.get("revenueGrowth"),
        "gross_margin": info.get("grossMargins"),
        "operating_margin": info.get("operatingMargins"),
        "free_cash_flow": info.get("freeCashflow"),
        "short_pct_float": info.get("shortPercentOfFloat"),
        "name": info.get("longName") or info.get("shortName") or ticker,
    }
    q["upside_pct"] = ((q["target_mean"] / price) - 1) * 100 if price and q["target_mean"] else None
    q["off_high_pct"] = ((price / q["high_52w"]) - 1) * 100 if price and q["high_52w"] else None

    try:
        closes = t.history(period="6mo")["Close"].dropna()
        def ret(n):
            return float(closes.iloc[-1] / closes.iloc[-1 - n] - 1) if len(closes) > n else None
        q["ret_1w"], q["ret_1m"], q["ret_3m"] = ret(5), ret(21), ret(63)
    except Exception:
        q["ret_1w"] = q["ret_1m"] = q["ret_3m"] = None

    q["next_earnings"] = None
    try:
        cal = t.calendar or {}
        ed = cal.get("Earnings Date") if isinstance(cal, dict) else None
        if ed:
            q["next_earnings"] = str(ed[0])
    except Exception:
        pass

    headlines = []
    try:
        for n in (t.news or [])[:8]:
            c = n.get("content", n)
            title = c.get("title")
            if title:
                headlines.append(f"{(c.get('pubDate') or '')[:10]} {title}".strip())
    except Exception:
        pass
    q["headlines"] = headlines
    return q


def _fmt_pct(x, mult=1.0):
    return "n/a" if x is None else f"{x * mult:+.1f}%"


def _build_prompt(h, q):
    pos = h.get("position_line", "")
    return f"""
You are the equity research analyst for the Frontier Agentic Trading System. Today is {date.today().isoformat()}.
Use Google Search to find the LATEST concrete developments (last ~30 days, with dates and numbers) for
{q['name']} ({h['ticker']}): earnings/guidance, product or contract news, analyst rating/target changes,
management commentary, insider selling, competitive or regulatory threats, and macro/sector drivers.

OUR THESIS for owning it:
"{h.get('thesis', 'Long-term frontier technology holding.')}"

OUR POSITION: {pos}

LIVE QUANT SNAPSHOT:
- Price ${q['price']}; 52w range ${q['low_52w']}–${q['high_52w']} ({_fmt_pct(q['off_high_pct'])} from high)
- 50DMA ${q['dma50']}, 200DMA ${q['dma200']}; returns 1w {_fmt_pct(q['ret_1w'], 100)}, 1m {_fmt_pct(q['ret_1m'], 100)}, 3m {_fmt_pct(q['ret_3m'], 100)}
- Analysts: {q['n_analysts']} covering, consensus {q['rec_key']} (mean {q['rec_mean']}); targets low ${q['target_low']} / mean ${q['target_mean']} / high ${q['target_high']} (mean implies {_fmt_pct(q['upside_pct'])})
- Valuation: fwd P/E {q['forward_pe']}, P/S {q['ps_ttm']}; revenue growth {_fmt_pct(q['revenue_growth'], 100)}; gross margin {_fmt_pct(q['gross_margin'], 100)}; op margin {_fmt_pct(q['operating_margin'], 100)}
- Next earnings: {q['next_earnings']}
- Recent headlines: {json.dumps(q['headlines'])}

RULES: Price alone never breaks a thesis — judge thesis_status on fundamentals and business facts.
Be specific (dates, $ figures, % growth, firm names). No generic company descriptions. No clichés.
Never use the phrase "in plain English". Do not invent facts; if search finds nothing new, say so.

Return ONLY a JSON object (no markdown fences) with exactly these keys:
{{
  "whats_going_on": "2-4 sentences on what is actually happening with the company right now",
  "supports_thesis": ["2-4 specific facts that SUPPORT our thesis"],
  "refutes_thesis": ["2-4 specific facts/risks that REFUTE or threaten our thesis (valuation counts)"],
  "thesis_status": "INTACT" | "WEAKENING" | "BROKEN",
  "news_score": <number from -2.0 (very negative) to 2.0 (very positive) for news flow vs our thesis>,
  "how_to_act": "1-2 sentences: concrete action for this position and the level/event that would change it",
  "what_this_means": "1-2 simple sentences for Jake explaining the bottom line"
}}
"""


def _parse_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            return json.loads(m.group(0))
        raise


class SentimentAgent:
    def __init__(self, max_workers=6):
        self.max_workers = max_workers
        self.client = None
        try:
            from google import genai
            from google.genai import types
            self._types = types
            if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
                self.client = genai.Client()
            else:
                print("WARNING: GEMINI_API_KEY not set — SentimentAgent runs QUANT-ONLY (thesis layer disabled).")
        except Exception as e:
            print(f"WARNING: google-genai unavailable ({e}) — QUANT-ONLY mode.")

    def _llm(self, h, q):
        if not self.client:
            return None, "Thesis layer offline (no GEMINI_API_KEY)."
        try:
            resp = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=_build_prompt(h, q),
                config=self._types.GenerateContentConfig(
                    tools=[self._types.Tool(google_search=self._types.GoogleSearch())],
                ),
            )
            data = _parse_json(resp.text)
            data["news_score"] = sc._clamp(float(data.get("news_score", 0)))
            status = str(data.get("thesis_status", "INTACT")).upper()
            data["thesis_status"] = status if status in ("INTACT", "WEAKENING", "BROKEN") else "INTACT"
            for k in ("whats_going_on", "how_to_act", "what_this_means"):
                data[k] = _clean(data.get(k, ""))
            for k in ("supports_thesis", "refutes_thesis"):
                data[k] = [_clean(x) for x in (data.get(k) or []) if x][:4]
            return data, None
        except Exception as e:
            return None, f"Thesis layer failed: {e}"

    def analyze(self, h, self_managed_tickers):
        ticker = h["ticker"]
        today = date.today()
        try:
            q = fetch_quant(ticker)
        except Exception as e:
            q = None
            print(f"  ✗ {ticker}: quant fetch failed ({e})")

        if not q or not q.get("price"):
            overlay = sc.rule_overlay(h, None, None, self_managed_tickers, today.isoformat())
            return {"ticker": ticker, "rating": None, "score_5": None, "composite": None,
                    "factors": {}, "quant": q or {}, "llm": None, "llm_error": "No live quote — fail-closed.",
                    "overlay": overlay, **_legacy(q, None)}

        llm, llm_err = self._llm(h, q)
        factors = {
            "news_thesis": llm["news_score"] if llm else None,
            "technical": sc.score_technical(q["price"], q["dma50"], q["dma200"], q["ret_1m"]),
            "analyst": sc.score_analyst(q["rec_mean"], q["n_analysts"]),
            "target": sc.score_target(q["upside_pct"], q["n_analysts"]),
        }
        comp, weights = sc.composite_score(factors)
        rating, color = sc.rating_for(comp) if comp is not None else (None, "#5F6368")
        thesis_status = llm["thesis_status"] if llm else "INTACT"

        dte = None
        if q.get("next_earnings"):
            try:
                dte = (datetime.strptime(q["next_earnings"][:10], "%Y-%m-%d").date() - today).days
            except Exception:
                pass
        overlay = sc.rule_overlay(h, rating, thesis_status, self_managed_tickers, today.isoformat(), dte)

        print(f"  ✓ {ticker}: {rating or 'UNRATED'} ({comp}) → {overlay['action']}" + (" [quant-only]" if not llm else ""))
        return {
            "ticker": ticker,
            "rating": rating,
            "rating_color": color,
            "composite": comp,
            "score_5": round(comp + 3, 2) if comp is not None else None,
            "factors": factors,
            "weights": weights,
            "quant": q,
            "llm": llm,
            "llm_error": llm_err,
            "thesis_status": thesis_status if llm else "UNVERIFIED",
            "days_to_earnings": dte,
            "overlay": overlay,
            **_legacy(q, llm),
        }

    def run(self, holdings):
        """
        holdings: list of dicts {ticker, account ('agentic'|'self_managed'), kind ('stock'|'option'),
                  shares, pnl_pct, pct_portfolio, thesis, position_line, option_side}
        A ticker can appear more than once (e.g. ONDS stock in Agentic + ONDS call in Self-Managed);
        the data fetch is shared and the overlay is computed per holding.
        Returns {ticker: result} for stocks, and {"<ticker>:option:<account>": result} for options.
        """
        print(f"SentimentAgent: rating {len(holdings)} holdings with {GEMINI_MODEL}...")
        sm_tickers = {h["ticker"] for h in holdings if h["account"] == "self_managed"}
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            results = list(ex.map(lambda h: self.analyze(h, sm_tickers), holdings))
        out = {}
        for h, r in zip(holdings, results):
            out[holding_key(h)] = r
        return out


def holding_key(h):
    return h["ticker"] if h.get("kind", "stock") == "stock" else f"{h['ticker']}:option:{h['account']}"


def _legacy(q, llm):
    """Backwards-compatible fields used by PortfolioManagerAgent / older builders."""
    q = q or {}
    return {
        "current_price": q.get("price") or 0,
        "target_mean": q.get("target_mean") or 0,
        "recommendation": q.get("rec_key") or "N/A",
        "upside_pct": q.get("upside_pct") or 0,
        "analysis": (llm or {}).get("whats_going_on") or "Thesis layer unavailable — rating is quant-only.",
    }


if __name__ == "__main__":
    # Quick test: python scripts/agents/sentiment_agent.py CRWD
    tick = sys.argv[1] if len(sys.argv) > 1 else "CRWD"
    res = SentimentAgent().analyze({"ticker": tick, "account": "self_managed", "kind": "stock",
                                    "shares": 0, "pnl_pct": 0, "pct_portfolio": 0}, set())
    print(json.dumps({k: v for k, v in res.items() if k != "quant"}, indent=2, default=str))
