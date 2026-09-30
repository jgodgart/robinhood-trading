#!/usr/bin/env python3
"""
run_all_briefs.py — Master Orchestration Script
1. Connects to Robinhood live via robin_stocks to pull fresh broker data and balances.
2. Updates local state (claude/robinhood-live-state.json and claude/account-snapshot.md).
3. Generates all email-safe charts with unified Y-axis scales and two-tone zero-crossings.
4. Dispatches all 3 morning briefs to jgodgart@gmail.com with embedded images via CID.
"""

import os
import sys
import subprocess
from datetime import datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
BRIEFS_DIR = os.path.join(BASE_DIR, "briefs")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def main():
    log("==================================================================")
    log("🚀 FRONTIER AGENTIC SYSTEM: FULL 3-BRIEF EXECUTION PASS")
    log("==================================================================")

    # -----------------------------------------------------------------
    # STEP 0: PULL LIVE ROBINHOOD BROKER DATA (MANDATORY ON EVERY RUN)
    # -----------------------------------------------------------------
    log("STEP 0: Connecting to Robinhood live to pull fresh holdings & equity...")
    sync_script = os.path.join(SCRIPTS_DIR, "robinhood_sync.py")
    res_sync = subprocess.run([sys.executable, sync_script], capture_output=True, text=True)
    print(res_sync.stdout)
    if res_sync.returncode != 0:
        log(f"⚠️ Robinhood sync returned code {res_sync.returncode}: {res_sync.stderr}")
    else:
        log("✅ Robinhood live sync complete. Fresh broker actuals confirmed.")

    # -----------------------------------------------------------------
    # STEP 1: GENERATE ALL HIGH-RESOLUTION CHARTS (UNIFIED Y-AXIS SCALES)
    # -----------------------------------------------------------------
    log("STEP 1: Generating high-resolution charts with unified Y-axis scales...")
    chart_script = os.path.join(SCRIPTS_DIR, "generate_chart_images.py")
    res_chart = subprocess.run([sys.executable, chart_script], capture_output=True, text=True)
    if res_chart.returncode != 0:
        log(f"❌ Chart generation failed: {res_chart.stderr}")
        sys.exit(1)
    log("✅ All high-resolution chart assets generated with two-tone zero-crossing.")

    # -----------------------------------------------------------------
    # STEP 1.5: REBUILD AGENTIC BRIEF HTML FROM FRESH BROKER DATA
    # -----------------------------------------------------------------
    log("STEP 1.5: Rebuilding Agentic Morning Briefing HTML with live broker data...")
    build_script = os.path.join(SCRIPTS_DIR, "build_agentic_brief.py")
    res_build = subprocess.run([sys.executable, build_script], capture_output=True, text=True)
    if res_build.returncode != 0:
        log(f"❌ Brief build failed: {res_build.stderr}")
    else:
        log("✅ Agentic Morning Briefing HTML updated with all 20 real stocks.")

    # -----------------------------------------------------------------
    # STEP 2: DISPATCH ALL 3 BRIEFINGS VIA EMAIL
    # -----------------------------------------------------------------
    log("STEP 2: Dispatching all 3 briefings to Jake Godgart (jgodgart@gmail.com)...")
    send_script = os.path.join(SCRIPTS_DIR, "send_brief_email.py")

    briefs_to_send = [
        ("Macro Market Pulse", os.path.join(BRIEFS_DIR, "2026-09-30-market-brief.html")),
        ("Self-Managed Account Digest", os.path.join(BRIEFS_DIR, "2026-09-30-core-brief.html")),
        ("Agentic Morning Briefing", os.path.join(BRIEFS_DIR, "2026-09-30-premarket-brief.html")),
    ]

    success_count = 0
    for name, brief_path in briefs_to_send:
        if not os.path.exists(brief_path):
            log(f"❌ Brief file not found: {brief_path}")
            continue

        log(f"📧 Dispatching {name} ({os.path.basename(brief_path)})...")
        res_send = subprocess.run([sys.executable, send_script, brief_path], capture_output=True, text=True)
        print(res_send.stdout)
        if res_send.returncode == 0 and "Successfully sent" in res_send.stdout:
            log(f"✅ {name} sent successfully!")
            success_count += 1
        else:
            log(f"❌ Error sending {name}: {res_send.stderr}")

    log("==================================================================")
    log(f"🏁 RUN COMPLETE: {success_count}/{len(briefs_to_send)} briefings dispatched successfully!")
    log("==================================================================")

if __name__ == "__main__":
    main()
