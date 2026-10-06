import logging
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

import os
import json
import logging
logging.getLogger('yfinance').setLevel(logging.CRITICAL)
import sys
import subprocess
from datetime import datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
STATE_FILE = os.path.join(BASE_DIR, "claude", "robinhood-live-state.json")
AGENTS_MD = os.path.join(BASE_DIR, "AGENTS.md")

sys.path.append(SCRIPTS_DIR)
from agents.macro_agent import MacroAgent
from agents.sentiment_agent import SentimentAgent
from agents.portfolio_manager_agent import PortfolioManagerAgent
from html_builders import build_macro_brief, build_agentic_brief, build_individual_brief

def main(dry_run=False):
    print("🚀 Starting Frontier Agentic Trading System Orchestrator...")
    
    print("STEP 0: Downloading live actuals from Google Drive...")
    
    # Run the secure Google Drive downloader
    try:
        subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "download_drive_state.py")], check=True)
    except Exception as e:
        print("Skipping download due to error:", e)
    
    if not os.path.exists(STATE_FILE):
        print(f"❌ Error: {STATE_FILE} not found after download attempt.")
        sys.exit(1)
        
    print("STEP 1: Generating charts...")
    subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "generate_chart_images.py")])
    
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
        
    print("STEP 2: Spawning AI Agents...")
    
    macro_agent = MacroAgent()
    macro_html = macro_agent.run()
    
    holdings_to_analyze = []
    
    # helper to format position line
    def fmt_pos(h):
        return f"{h.get('shares',0):.2f} shares at ${h.get('average_cost',0):.2f} (PNL: {h.get('pnl_pct',0):+.1f}%)"
    def fmt_opt(o):
        return f"{o.get('quantity',0)} contracts at ${o.get('avg_cost',0):.2f} (PNL: {o.get('total_pnl_pct',0):+.1f}%)"
    
    for s in state.get('agentic', {}).get('stocks', []):
        holdings_to_analyze.append({
            "ticker": s["ticker"], "account": "agentic", "kind": "stock",
            "shares": s.get("shares", 0), "pnl_pct": s.get("pnl_pct", 0), "pct_portfolio": s.get("pct_portfolio", 0),
            "position_line": fmt_pos(s)
        })
    for o in state.get('agentic', {}).get('options', []):
        holdings_to_analyze.append({
            "ticker": o["underlying"], "account": "agentic", "kind": "option", "option_side": "short" if o.get("quantity", 1) < 0 else "long",
            "shares": o.get("quantity", 0), "pnl_pct": o.get("total_pnl_pct", 0), "pct_portfolio": 0,
            "position_line": fmt_opt(o)
        })
        
    for s in state.get('individual', state.get('self_managed', {})).get('stocks', []):
        holdings_to_analyze.append({
            "ticker": s["ticker"], "account": "self_managed", "kind": "stock",
            "shares": s.get("shares", 0), "pnl_pct": s.get("pnl_pct", 0), "pct_portfolio": s.get("pct_portfolio", 0),
            "position_line": fmt_pos(s)
        })
    for o in state.get('individual', state.get('self_managed', {})).get('options', []):
        holdings_to_analyze.append({
            "ticker": o["underlying"], "account": "self_managed", "kind": "option", "option_side": "short" if o.get("quantity", 1) < 0 else "long",
            "shares": o.get("quantity", 0), "pnl_pct": o.get("total_pnl_pct", 0), "pct_portfolio": 0,
            "position_line": fmt_opt(o)
        })
        
    # Trim for faster testing during development if needed
    # holdings_to_analyze = holdings_to_analyze[:2]
    
    sentiment_agent = SentimentAgent()
    sentiment_data = sentiment_agent.run(holdings_to_analyze)
    
    pm_agent = PortfolioManagerAgent(STATE_FILE, AGENTS_MD)
    tactical_html = pm_agent.run(sentiment_data)
    
    print("STEP 3: Building HTML Reports...")
    macro_brief_path = build_macro_brief(macro_html)
    agentic_brief_path = build_agentic_brief(STATE_FILE, sentiment_data, tactical_html)
    indiv_brief_path = build_individual_brief(STATE_FILE, sentiment_data)
    
    print("STEP 4: Dispatching Emails...")
    briefs_to_send = [
        ("1/3: Macroeconomy Brief", macro_brief_path),
        ("2/3: Agentic Portfolio", agentic_brief_path),
        ("3/3: Individual Portfolio", indiv_brief_path)
    ]
    
    if dry_run:
        print("Dry run enabled. Skipping email dispatch.")
    else:
        send_script = os.path.join(SCRIPTS_DIR, "send_brief_email.py")
        for name, brief_path in briefs_to_send:
            print(f"Dispatching {name}...")
            subprocess.run([sys.executable, send_script, brief_path])
        
    print("🏁 Orchestrator complete.")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
