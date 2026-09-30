import os
import json
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
    subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "download_drive_state.py")], check=True)
    
    if not os.path.exists(STATE_FILE):
        print(f"❌ Error: {STATE_FILE} not found after download attempt.")
        sys.exit(1)
        
    print("STEP 1: Generating charts...")
    subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "generate_chart_images.py")])
    
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
        
    agentic_stocks = [s['ticker'] for s in state.get('agentic', {}).get('stocks', [])]
    individual_stocks = [s['ticker'] for s in state.get('individual', {}).get('stocks', [])]
    all_tickers = list(set(agentic_stocks + individual_stocks))
    
    # Trim for faster testing during development if needed
    # all_tickers = all_tickers[:2]
    
    print("STEP 2: Spawning AI Agents...")
    
    macro_agent = MacroAgent()
    macro_html = macro_agent.run()
    
    sentiment_agent = SentimentAgent()
    sentiment_data = sentiment_agent.run(all_tickers)
    
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
