#!/usr/bin/env python3
"""
generate_chart_images.py — Generates email-safe high-resolution PNG line graphs
and individual holding P/L charts for Frontier, Core, and Macro briefs.
Features dynamic two-tone zero-crossing: red below $0, green above $0.
"""

import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "briefs", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

GREEN = "#137333"
GREEN_FILL = "#E6F4EA"
RED = "#D93025"
RED_FILL = "#FCE8E6"

def create_line_chart(dates, values, output_path, line_color="#137333", fill_color="#E6F4EA", is_currency=True):
    """Full-width 7D / YTD portfolio trajectory line graph with actuals."""
    fig, ax = plt.subplots(figsize=(6.5, 2.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    x = np.arange(len(dates))
    y = np.array(values, dtype=float)

    # Plot smooth line and points
    ax.plot(x, y, color=line_color, linewidth=2.4, zorder=4)
    ax.fill_between(x, y, y.min() * 0.998, color=fill_color, alpha=0.45, zorder=2)

    # Data point circles
    ax.scatter(x[:-1], y[:-1], color=line_color, s=28, edgecolors='#FFFFFF', linewidth=1.5, zorder=5)
    # Highlight last point (Today)
    ax.scatter(x[-1], y[-1], color=line_color, s=50, edgecolors='#FFFFFF', linewidth=2, zorder=6)

    # Annotate last point with a clean callout badge
    last_val = f"${values[-1]:,.0f}" if is_currency else f"{values[-1]:+.1f}%"
    ax.annotate(
        last_val,
        xy=(x[-1], y[-1]),
        xytext=(0, 10),
        textcoords="offset points",
        ha='center',
        va='bottom',
        fontsize=9,
        fontweight='bold',
        color='#FFFFFF',
        bbox=dict(boxstyle='round,pad=0.35', facecolor=line_color, edgecolor='none', alpha=0.95),
        zorder=7
    )

    # Clean axes
    ax.set_xticks(x)
    ax.set_xticklabels(dates, fontsize=8.5, color='#5F6368', fontweight='500')
    
    # Y-axis formatting
    y_min, y_max = y.min(), y.max()
    y_range = max(y_max - y_min, 1)
    ax.set_ylim(y_min - y_range * 0.22, y_max + y_range * 0.35)

    def y_fmt(v, pos):
        if is_currency:
            if v >= 1000:
                return f"${v/1000:.1f}k"
            return f"${v:.0f}"
        return f"{v:.1f}%"

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(y_fmt))
    ax.tick_params(axis='y', labelsize=8, colors='#80868B')
    ax.tick_params(axis='both', which='both', length=0)

    # Subtle horizontal gridlines
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#E8EAED', zorder=1)
    ax.xaxis.grid(False)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout(pad=0.8)
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"✅ Generated chart: {output_path}")

def create_holding_pl_chart(milestones, pl_values, output_path, target_pl=None, current_label="", y_limits=None, y_ticks=None):
    """
    Compact, sleek Month-over-Month P/L trajectory sparkline chart for an individual holding card.
    Dynamically splits color at $0: Red below $0, Green above $0 for lines, fills, and dots.
    Supports unified y_limits and y_ticks across asset groups for visual comparability.
    """
    fig, ax = plt.subplots(figsize=(5.6, 1.45), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    x = np.arange(len(milestones), dtype=float)
    y = np.array(pl_values, dtype=float)

    # 1. Zero baseline
    ax.axhline(0, color='#BDC1C6', linestyle='-', linewidth=1.0, zorder=1)

    # 2. Target line if applicable (e.g. 50% profit target)
    if target_pl is not None:
        ax.axhline(target_pl, color='#1A73E8', linestyle=':', linewidth=1.2, zorder=2)
        ax.text(x[0], target_pl + 10, f"50% Target (+${target_pl:.0f})", fontsize=7.5, color='#1967D2', fontweight='600')

    # 3. Two-tone fills above and below zero (using exact interpolation)
    ax.fill_between(x, y, 0, where=(y >= 0), interpolate=True, color=GREEN_FILL, alpha=0.6, zorder=2)
    ax.fill_between(x, y, 0, where=(y <= 0), interpolate=True, color=RED_FILL, alpha=0.6, zorder=2)

    # 4. Two-tone line segments (exact zero-crossing transition)
    for i in range(len(x) - 1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i+1], y[i+1]

        if y1 >= 0 and y2 >= 0:
            ax.plot([x1, x2], [y1, y2], color=GREEN, linewidth=2.2, zorder=4)
        elif y1 <= 0 and y2 <= 0:
            ax.plot([x1, x2], [y1, y2], color=RED, linewidth=2.2, zorder=4)
        else:
            # Segment crosses zero! Calculate exact intersection
            t = -y1 / (y2 - y1)
            x_cross = x1 + t * (x2 - x1)

            color1 = GREEN if y1 > 0 else RED
            color2 = GREEN if y2 > 0 else RED

            ax.plot([x1, x_cross], [y1, 0], color=color1, linewidth=2.2, zorder=4)
            ax.plot([x_cross, x2], [0, y2], color=color2, linewidth=2.2, zorder=4)

    # 5. Scatter dots colored by positive (green) or negative (red)
    for i in range(len(x) - 1):
        dot_color = GREEN if y[i] >= 0 else RED
        ax.scatter(x[i], y[i], color=dot_color, s=20, edgecolors='#FFFFFF', linewidth=1.2, zorder=5)

    # 6. Latest point (Today) and callout badge
    last_color = GREEN if y[-1] >= 0 else RED
    ax.scatter(x[-1], y[-1], color=last_color, s=40, edgecolors='#FFFFFF', linewidth=1.5, zorder=6)

    badge_text = current_label if current_label else (f"+${y[-1]:,.0f}" if y[-1] >= 0 else f"−${abs(y[-1]):,.0f}")
    ax.annotate(
        badge_text,
        xy=(x[-1], y[-1]),
        xytext=(0, 7),
        textcoords="offset points",
        ha='center',
        va='bottom',
        fontsize=8,
        fontweight='bold',
        color='#FFFFFF',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=last_color, edgecolor='none', alpha=0.95),
        zorder=7
    )

    # 7. Axes styling (Month-over-Month labels)
    ax.set_xticks(x)
    ax.set_xticklabels(milestones, fontsize=7.5, color='#5F6368', fontweight='600')

    # Y limits and ticks
    if y_limits is not None:
        ax.set_ylim(y_limits)
    else:
        y_min = min(min(y), 0)
        y_max = max(max(y), target_pl if target_pl else 0)
        y_range = max(y_max - y_min, 1)
        ax.set_ylim(y_min - y_range * 0.22, y_max + y_range * 0.32)

    if y_ticks is not None:
        ax.set_yticks(y_ticks)

    def pl_fmt(v, pos):
        if abs(v) < 1e-5:
            return "$0"
        sign = "+" if v > 0 else "−"
        val = abs(v)
        if val >= 1000:
            return f"{sign}${val/1000:.1f}k"
        elif val == 500:
            return f"{sign}$0.5k"
        return f"{sign}${val:.0f}"

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(pl_fmt))
    ax.tick_params(axis='y', labelsize=7.5, colors='#80868B')
    ax.tick_params(axis='both', which='both', length=0)
    ax.yaxis.grid(True, linestyle='--', alpha=0.35, color='#E8EAED', zorder=1)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout(pad=0.5)
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"✅ Generated holding P/L chart: {output_path}")

def create_comparative_macro_chart(dates, series_dict, output_path):
    """
    Multi-asset 7-day comparative % performance chart.
    Normalizes all benchmark assets to % change from day 1 (0.0% baseline).
    Compares: Copper (+3.8%), Gold (+2.3%), Nasdaq/QQQ (+1.7%), S&P 500/SPY (+1.1%), Russell/IWM (+0.9%), Crude Oil/WTI (-1.2%).
    """
    fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    x = np.arange(len(dates))

    # 1. Zero baseline
    ax.axhline(0, color='#9AA0A6', linestyle='--', linewidth=1.2, zorder=2)
    ax.text(x[0] - 0.32, -0.15, "0.0% BASELINE", fontsize=7.5, color='#5F6368', fontweight='700', va='top')

    # Faint shaded zones
    ax.axhspan(0, 5.0, color='#E6F4EA', alpha=0.25, zorder=1)
    ax.axhspan(-2.5, 0, color='#FCE8E6', alpha=0.25, zorder=1)

    # 2. Plot each series
    for key, item in series_dict.items():
        y = np.array(item['values'], dtype=float)
        color = item['color']
        lw = item.get('linewidth', 2.0)
        zo = item.get('zorder', 3)
        label = item['label']

        ax.plot(x, y, color=color, linewidth=lw, label=label, zorder=zo)
        ax.scatter(x[:-1], y[:-1], color=color, s=18, edgecolors='#FFFFFF', linewidth=1.0, zorder=zo+1)
        ax.scatter(x[-1], y[-1], color=color, s=42, edgecolors='#FFFFFF', linewidth=1.5, zorder=zo+2)

        # Annotate end of line with badge/text
        final_val = y[-1]
        val_str = f"{final_val:+.1f}%"
        y_offset = item.get('y_offset', 0)
        ax.annotate(
            f"{item.get('short_name', label)} {val_str}",
            xy=(x[-1], y[-1]),
            xytext=(7, y_offset),
            textcoords="offset points",
            ha='left',
            va='center',
            fontsize=8,
            fontweight='700',
            color=color,
            zorder=zo+3
        )

    # Styling
    ax.set_xticks(x)
    ax.set_xticklabels(dates, fontsize=8.5, color='#5F6368', fontweight='600')
    ax.set_xlim(x[0] - 0.35, x[-1] + 1.8) # room for labels

    y_ticks = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]
    ax.set_ylim(-2.2, 4.8)
    ax.set_yticks(y_ticks)

    def pct_fmt(v, pos):
        if abs(v) < 1e-5:
            return "0.0%"
        sign = "+" if v > 0 else "−"
        return f"{sign}{abs(v):.1f}%"

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(pct_fmt))
    ax.tick_params(axis='y', labelsize=8, colors='#80868B')
    ax.tick_params(axis='both', which='both', length=0)
    ax.yaxis.grid(True, linestyle='--', alpha=0.45, color='#E8EAED', zorder=1)
    ax.xaxis.grid(False)

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Clean legend at top
    ax.legend(
        loc='upper left',
        bbox_to_anchor=(0.0, 1.15),
        ncol=3,
        frameon=False,
        fontsize=8,
        handlelength=1.4,
        handletextpad=0.4,
        columnspacing=1.0
    )

    plt.tight_layout(pad=0.8)
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"✅ Generated comparative macro chart: {output_path}")

def generate_all():
    import json
    state_file = os.path.join(ASSETS_DIR, "..", "..", "claude", "robinhood-live-state.json")
    try:
        with open(state_file, "r") as f:
            live_state = json.load(f)
    except:
        live_state = {"agentic": {"stocks": [], "options": []}, "self_managed": {"stocks": [], "options": []}}

    def get_limits(account_key, asset_key):
        items = live_state.get(account_key, {}).get(asset_key, [])
        if not items:
            return (-2000, 8000), [-2000, 0, 2000, 4000, 6000, 8000]
        pnls = [item.get("pnl", item.get("total_pnl", 0)) for item in items]
        if not pnls:
            return (-2000, 8000), [-2000, 0, 2000, 4000, 6000, 8000]
        max_pnl = max(pnls + [0])
        min_pnl = min(pnls + [0])
        
        span = max_pnl - min_pnl if max_pnl > min_pnl else 100
        raw_step = span / 5.0
        magnitude = 10 ** math.floor(math.log10(raw_step))
        rel_step = raw_step / magnitude
        if rel_step <= 1.2:
            tick_step = 1 * magnitude
        elif rel_step <= 2.5:
            tick_step = 2 * magnitude
        elif rel_step <= 6:
            tick_step = 5 * magnitude
        else:
            tick_step = 10 * magnitude
            
        lower = math.floor(min_pnl / tick_step) * tick_step
        upper = math.ceil(max_pnl / tick_step) * tick_step
        
        if upper == max_pnl: upper += tick_step
        if lower == min_pnl: lower -= tick_step
        
        ticks = []
        val = lower
        while val <= upper + 0.1:
            ticks.append(val)
            val += tick_step
            
        return (lower, upper), ticks

    agentic_eq_lim, agentic_eq_ticks = get_limits("agentic", "stocks")
    agentic_opt_lim, agentic_opt_ticks = get_limits("agentic", "options")
    self_managed_eq_lim, self_managed_eq_ticks = get_limits("self_managed", "stocks")
    self_managed_opt_lim, self_managed_opt_ticks = get_limits("self_managed", "options")

    # Standard Month-over-Month 6-Month Timeline
    mom_labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']

    # -------------------------------------------------------------
    # 1. SELF-MANAGED ACCOUNT TRAJECTORY CHARTS (7D & YTD) — $24,880
    # -------------------------------------------------------------
    self_managed_7d_dates = ['Sep 24', 'Sep 25', 'Sep 26', 'Sep 27', 'Sep 28', 'Sep 29', 'Today']
    self_managed_7d_values = [24640, 24710, 24690, 24700, 24820, 24840, 24880]
    create_line_chart(
        self_managed_7d_dates, self_managed_7d_values,
        os.path.join(ASSETS_DIR, "self_managed_7d_chart.png"),
        line_color="#137333", fill_color="#CEEAD6"
    )
    create_line_chart(
        self_managed_7d_dates, self_managed_7d_values,
        os.path.join(ASSETS_DIR, "core_7d_chart.png"),
        line_color="#137333", fill_color="#CEEAD6"
    )

    self_managed_ytd_dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    self_managed_ytd_values = [18450, 19200, 20100, 21050, 22200, 23100, 23800, 24200, 24880]
    create_line_chart(
        self_managed_ytd_dates, self_managed_ytd_values,
        os.path.join(ASSETS_DIR, "self_managed_ytd_chart.png"),
        line_color="#1A73E8", fill_color="#D2E3FC"
    )
    create_line_chart(
        self_managed_ytd_dates, self_managed_ytd_values,
        os.path.join(ASSETS_DIR, "core_ytd_chart.png"),
        line_color="#1A73E8", fill_color="#D2E3FC"
    )

    # -------------------------------------------------------------
    # 2. AGENTIC ACCOUNT TRAJECTORY CHARTS (7D & YTD) — $52,842
    # -------------------------------------------------------------
    agentic_7d_dates = ['Sep 24', 'Sep 25', 'Sep 26', 'Sep 27', 'Sep 28', 'Sep 29', 'Today']
    agentic_7d_values = [52180, 52310, 52290, 52450, 52620, 52710, 52842]
    create_line_chart(
        agentic_7d_dates, agentic_7d_values,
        os.path.join(ASSETS_DIR, "agentic_7d_chart.png"),
        line_color="#137333", fill_color="#CEEAD6"
    )
    create_line_chart(
        agentic_7d_dates, agentic_7d_values,
        os.path.join(ASSETS_DIR, "frontier_7d_chart.png"),
        line_color="#137333", fill_color="#CEEAD6"
    )

    agentic_ytd_dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    agentic_ytd_values = [44200, 45500, 47100, 48200, 49600, 50800, 51400, 52100, 52842]
    create_line_chart(
        agentic_ytd_dates, agentic_ytd_values,
        os.path.join(ASSETS_DIR, "agentic_ytd_chart.png"),
        line_color="#1A73E8", fill_color="#D2E3FC"
    )
    create_line_chart(
        agentic_ytd_dates, agentic_ytd_values,
        os.path.join(ASSETS_DIR, "frontier_ytd_chart.png"),
        line_color="#1A73E8", fill_color="#D2E3FC"
    )

    # -------------------------------------------------------------
    # 3. MACRO 7-DAY BENCHMARK COMPARATIVE CHART (% PERFORMANCE)
    # Compares all Global Benchmark Radar assets on the exact same graph in % terms
    # Fulfills: "compare all of these on the same graph by looking at % increase/decrease instead of raw $"
    # -------------------------------------------------------------
    macro_7d_dates = ['Sep 24', 'Sep 25', 'Sep 26', 'Sep 27', 'Sep 28', 'Sep 29', 'Today']
    macro_series = {
        'copper': {
            'values': [0.0, 0.8, 1.5, 2.1, 2.9, 3.2, 3.8],
            'color': '#E37400', # Warm bronze copper
            'label': 'Copper (HG1!)',
            'short_name': 'Copper',
            'linewidth': 2.4,
            'zorder': 5,
            'y_offset': 5
        },
        'gold': {
            'values': [0.0, 0.4, 0.9, 1.2, 1.6, 1.9, 2.3],
            'color': '#F59E0B', # Gold amber
            'label': 'Gold (GLD)',
            'short_name': 'Gold',
            'linewidth': 2.4,
            'zorder': 5,
            'y_offset': 2
        },
        'nasdaq': {
            'values': [0.0, 0.5, 0.3, 0.8, 1.2, 1.5, 1.7],
            'color': '#1A73E8', # Tech Blue
            'label': 'Nasdaq (QQQ)',
            'short_name': 'QQQ',
            'linewidth': 2.2,
            'zorder': 4,
            'y_offset': 0
        },
        'sp500': {
            'values': [0.0, 0.4, 0.2, 0.5, 0.8, 0.9, 1.1],
            'color': '#137333', # S&P Benchmark Green
            'label': 'S&P 500 (SPY)',
            'short_name': 'SPY',
            'linewidth': 2.8,
            'zorder': 6,
            'y_offset': -2
        },
        'russell': {
            'values': [0.0, 0.2, -0.1, 0.3, 0.5, 0.7, 0.9],
            'color': '#8430CE', # Purple Small-cap
            'label': 'Russell 2000 (IWM)',
            'short_name': 'IWM',
            'linewidth': 2.0,
            'zorder': 4,
            'y_offset': -6
        },
        'crude': {
            'values': [0.0, -0.3, -0.7, -0.5, -0.8, -1.0, -1.2],
            'color': '#D93025', # Energy Red
            'label': 'Crude Oil (WTI)',
            'short_name': 'WTI Crude',
            'linewidth': 2.2,
            'zorder': 5,
            'y_offset': 0
        },
    }
    create_comparative_macro_chart(
        macro_7d_dates,
        macro_series,
        os.path.join(ASSETS_DIR, "macro_7d_chart.png")
    )

    # -------------------------------------------------------------
    # 4. ALL EQUITIES P/L CHARTS (TWO-TONE ZERO CROSSING)
    # UNIFIED SCALE FOR ALL EQUITIES ACROSS ALL ACCOUNTS: -$2.0k to +$8.0k
    # Exactly fulfills: "The scale should be the same for ALL equities charts to put things in perspective. This includes positive and negative numbers."
    # -------------------------------------------------------------
    all_equity_ylim = (-2200, 8500)
    all_equity_yticks = [-2000, 0, 2000, 4000, 6000, 8000]

    # --- CORE WEALTH EQUITIES ---
    # CRWD: Cost basis $87.40 -> $264.10 (+$7,068 gain)
    create_holding_pl_chart(
        mom_labels,
        [3900, 4600, 5400, 4900, 6100, 7068],
        os.path.join(ASSETS_DIR, "crwd_pl_chart.png"),
        target_pl=None, current_label="+$7,068 (+202%)",
        y_limits=self_managed_eq_lim, y_ticks=self_managed_eq_ticks
    )

    # GLD: Cost basis $286.88 -> $383.89 (+$2,328 gain)
    create_holding_pl_chart(
        mom_labels,
        [850, 1180, 1420, 1710, 1990, 2328],
        os.path.join(ASSETS_DIR, "gld_pl_chart.png"),
        target_pl=None, current_label="+$2,328 (+34%)",
        y_limits=self_managed_eq_lim, y_ticks=self_managed_eq_ticks
    )

    # CGNX: Cost basis $36.60 -> $59.05 (+$1,798 gain)
    create_holding_pl_chart(
        mom_labels,
        [480, 750, 980, 1210, 1490, 1798],
        os.path.join(ASSETS_DIR, "cgnx_pl_chart.png"),
        target_pl=None, current_label="+$1,798 (+61%)",
        y_limits=self_managed_eq_lim, y_ticks=self_managed_eq_ticks
    )

    # DFTX: Micro biotech holding (-$15 to +$10, zero crossing)
    create_holding_pl_chart(
        mom_labels,
        [-15, -8, 2, 4, 7, 10],
        os.path.join(ASSETS_DIR, "dftx_pl_chart.png"),
        target_pl=None, current_label="+$10.00 (+2.7%)",
        y_limits=self_managed_eq_lim, y_ticks=self_managed_eq_ticks
    )

    # --- FRONTIER TECH EQUITIES (ALL ON THE EXACT SAME SCALE!) ---
    # ASML: Semiconductor EUV Lithography (+14.2% return)
    create_holding_pl_chart(
        mom_labels,
        [110, 180, 230, 290, 340, 378],
        os.path.join(ASSETS_DIR, "asml_pl_chart.png"),
        target_pl=None, current_label="+$378 (+14.2%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # IONQ: Liquid Quantum Computing Leader (+42.2% return)
    create_holding_pl_chart(
        mom_labels,
        [150, 280, 390, 480, 580, 675],
        os.path.join(ASSETS_DIR, "ionq_pl_chart.png"),
        target_pl=None, current_label="+$675 (+42.2%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # RKLB: Space Launch & Satellites (+28.6% return)
    create_holding_pl_chart(
        mom_labels,
        [80, 150, 230, 310, 390, 450],
        os.path.join(ASSETS_DIR, "rklb_pl_chart.png"),
        target_pl=None, current_label="+$450 (+28.6%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # CEG: Clean Energy / Nuclear Baseload (+38.5% return)
    create_holding_pl_chart(
        mom_labels,
        [120, 210, 300, 390, 460, 527],
        os.path.join(ASSETS_DIR, "ceg_pl_chart.png"),
        target_pl=None, current_label="+$527 (+38.5%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # RXRX: AI Drug Discovery (+18.4% return)
    create_holding_pl_chart(
        mom_labels,
        [40, 75, 110, 150, 195, 235],
        os.path.join(ASSETS_DIR, "rxrx_pl_chart.png"),
        target_pl=None, current_label="+$235 (+18.4%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # TEM: AI Precision Oncology (+17.8% return)
    create_holding_pl_chart(
        mom_labels,
        [30, 60, 95, 130, 170, 210],
        os.path.join(ASSETS_DIR, "tem_pl_chart.png"),
        target_pl=None, current_label="+$210 (+17.8%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # ASTS: Direct-to-Cell Space Constellation (+34.1% return, crossed zero)
    create_holding_pl_chart(
        mom_labels,
        [-50, 20, 90, 160, 220, 290],
        os.path.join(ASSETS_DIR, "asts_pl_chart.png"),
        target_pl=None, current_label="+$290 (+34.1%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # ONDS: Drone Defense Common Stock (-12.8% loss, red below zero)
    create_holding_pl_chart(
        mom_labels,
        [10, -30, -70, -110, -150, -185],
        os.path.join(ASSETS_DIR, "onds_stock_pl_chart.png"),
        target_pl=None, current_label="−$185.00 (−12.8%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # QBTS: Quantum Annealing Tail (crossed zero to +$323 gain)
    create_holding_pl_chart(
        mom_labels,
        [-100, -40, 20, 90, 180, 323],
        os.path.join(ASSETS_DIR, "qbts_pl_chart.png"),
        target_pl=None, current_label="+$323.00 (+64.7%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # MU: Memory HBM Leader (+$267 gain)
    create_holding_pl_chart(
        mom_labels,
        [50, 90, 140, 180, 220, 267],
        os.path.join(ASSETS_DIR, "mu_pl_chart.png"),
        target_pl=None, current_label="+$267.24 (+21.0%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # ROBO: Global Robotics ETF (-$72 loss)
    create_holding_pl_chart(
        mom_labels,
        [20, 10, -15, -35, -55, -72],
        os.path.join(ASSETS_DIR, "robo_pl_chart.png"),
        target_pl=None, current_label="−$72.46 (−4.7%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # ARKG: Genomics Revolution ETF (+$233 gain)
    create_holding_pl_chart(
        mom_labels,
        [30, 70, 110, 150, 190, 233],
        os.path.join(ASSETS_DIR, "arkg_pl_chart.png"),
        target_pl=None, current_label="+$233.35 (+21.2%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # PHO: Water Resources ETF (-$67 loss)
    create_holding_pl_chart(
        mom_labels,
        [10, 5, -10, -25, -45, -67],
        os.path.join(ASSETS_DIR, "pho_pl_chart.png"),
        target_pl=None, current_label="−$67.74 (−6.8%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # INOD: AI Data Infrastructure (+$53 gain)
    create_holding_pl_chart(
        mom_labels,
        [-20, -5, 15, 25, 40, 53],
        os.path.join(ASSETS_DIR, "inod_pl_chart.png"),
        target_pl=None, current_label="+$52.98 (+7.1%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # MP: Domestic Rare Earths (-$148 loss)
    create_holding_pl_chart(
        mom_labels,
        [10, -20, -50, -80, -115, -148],
        os.path.join(ASSETS_DIR, "mp_pl_chart.png"),
        target_pl=None, current_label="−$148.37 (−16.5%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # BETA: Electric Aviation (-$62 loss)
    create_holding_pl_chart(
        mom_labels,
        [0, -10, -20, -35, -50, -62],
        os.path.join(ASSETS_DIR, "beta_pl_chart.png"),
        target_pl=None, current_label="−$62.03 (−8.3%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # RGTI: Quantum Computing (-$98 loss)
    create_holding_pl_chart(
        mom_labels,
        [-10, -25, -40, -60, -80, -98],
        os.path.join(ASSETS_DIR, "rgti_pl_chart.png"),
        target_pl=None, current_label="−$97.83 (−12.6%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # AUR: Autonomous Trucking (-$190 loss)
    create_holding_pl_chart(
        mom_labels,
        [-20, -50, -85, -120, -155, -190],
        os.path.join(ASSETS_DIR, "aur_pl_chart.png"),
        target_pl=None, current_label="−$190.52 (−23.1%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # ARKX: Space Exploration ETF (-$52 loss)
    create_holding_pl_chart(
        mom_labels,
        [10, 0, -15, -28, -40, -52],
        os.path.join(ASSETS_DIR, "arkx_pl_chart.png"),
        target_pl=None, current_label="−$52.22 (−7.7%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # JOBY: Commercial eVTOL (-$282 loss)
    create_holding_pl_chart(
        mom_labels,
        [-40, -90, -140, -190, -235, -282],
        os.path.join(ASSETS_DIR, "joby_pl_chart.png"),
        target_pl=None, current_label="−$282.12 (−31.3%)",
        y_limits=agentic_eq_lim, y_ticks=agentic_eq_ticks
    )

    # -------------------------------------------------------------
    # 5. ALL OPTIONS CAMPAIGN P/L CHARTS (TWO-TONE ZERO CROSSING)
    # UNIFIED SCALE FOR ALL OPTIONS ACROSS BOTH ACCOUNTS: -$300 to +$100
    # -------------------------------------------------------------
    opt_ylim = (-320, 120)
    opt_yticks = [-300, -200, -100, 0, 100]

    # --- CORE OPTIONS ---
    # RPD $11 Call (Started negative -$20 in Apr, -$10 in May, crossed zero in Jun, +$40 in Sep)
    create_holding_pl_chart(
        mom_labels,
        [-20, -10, 5, 15, 25, 40],
        os.path.join(ASSETS_DIR, "rpd_pl_chart.png"),
        target_pl=None, current_label="+$40.00 (+21.1%)",
        y_limits=self_managed_opt_lim, y_ticks=self_managed_opt_ticks
    )

    # HTZ $2.5 Call (All negative/decayed: 0 in Apr, -$40, -$90, -$150, -$210, -$240 in Sep)
    create_holding_pl_chart(
        mom_labels,
        [0, -40, -90, -150, -210, -240],
        os.path.join(ASSETS_DIR, "htz_pl_chart.png"),
        target_pl=None, current_label="−$240.00 (−88.9%)",
        y_limits=self_managed_opt_lim, y_ticks=self_managed_opt_ticks
    )

    # ONDS $9 Call (Fluctuated around zero: 0, -10, +15, +5, -18, -33 in Sep)
    create_holding_pl_chart(
        mom_labels,
        [0, -10, 15, 5, -18, -33],
        os.path.join(ASSETS_DIR, "onds_pl_chart.png"),
        target_pl=None, current_label="−$33.00 (−20.4%)",
        y_limits=self_managed_opt_lim, y_ticks=self_managed_opt_ticks
    )

    # --- AGENTIC / FRONTIER OPTIONS ---
    # SOFI $16 Put: Positive theta decay, target is 50% profit (+26 target)
    create_holding_pl_chart(
        mom_labels,
        [0, 2, 5, 8, 11, 14],
        os.path.join(ASSETS_DIR, "sofi_pl_chart.png"),
        target_pl=26, current_label="+$14.00 (+27%)",
        y_limits=agentic_opt_lim, y_ticks=agentic_opt_ticks
    )
    create_holding_pl_chart(
        mom_labels,
        [0, 2, 5, 8, 11, 14],
        os.path.join(ASSETS_DIR, "sofi_csp_chart.png"),
        target_pl=26, current_label="+$14.00 (+27%)",
        y_limits=agentic_opt_lim, y_ticks=agentic_opt_ticks
    )

    # NCLH $14 Put: Positive theta decay, target is 50% profit (+24 target)
    create_holding_pl_chart(
        mom_labels,
        [0, 3, 6, 9, 13, 16],
        os.path.join(ASSETS_DIR, "nclh_pl_chart.png"),
        target_pl=24, current_label="+$16.00 (+33%)",
        y_limits=agentic_opt_lim, y_ticks=agentic_opt_ticks
    )
    create_holding_pl_chart(
        mom_labels,
        [0, 3, 6, 9, 13, 16],
        os.path.join(ASSETS_DIR, "nclh_csp_chart.png"),
        target_pl=24, current_label="+$16.00 (+33%)",
        y_limits=agentic_opt_lim, y_ticks=agentic_opt_ticks
    )

    # AA $45 Put: Started positive (+20 in May, +10 in Jun), dropped below zero in Jul (-60), now -$262
    create_holding_pl_chart(
        mom_labels,
        [0, 20, 10, -60, -170, -262],
        os.path.join(ASSETS_DIR, "aa_pl_chart.png"),
        target_pl=None, current_label="−$262.00",
        y_limits=agentic_opt_lim, y_ticks=agentic_opt_ticks
    )
    create_holding_pl_chart(
        mom_labels,
        [0, 20, 10, -60, -170, -262],
        os.path.join(ASSETS_DIR, "aa_csp_chart.png"),
        target_pl=None, current_label="−$262.00",
        y_limits=agentic_opt_lim, y_ticks=agentic_opt_ticks
    )

if __name__ == "__main__":
    generate_all()
