#!/usr/bin/env python3
"""
Robinhood Live Account Synchronizer
Connects directly to Robinhood via robin_stocks to pull actual stock holdings,
open options positions, and portfolio equity for BOTH accounts:
- Self-Managed Account: 5PY51143 (••••1143)
- Agentic Account: 865935530 (••••5530)
"""

import sys
import os
import json
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

def get_robinhood_client():
    try:
        import robin_stocks.robinhood as r
        return r
    except ImportError:
        print("❌ robin_stocks is not installed in the active environment.")
        print("Run: .venv/bin/pip install robin_stocks")
        sys.exit(1)

def interactive_login(username=None, password=None):
    r = get_robinhood_client()
    print("🔐 Robinhood Live Authentication")
    print("--------------------------------")
    if not username:
        username = input("Robinhood Username / Email: ").strip()
    if not password:
        import getpass
        password = getpass.getpass("Robinhood Password: ").strip()
    
    try:
        print("Sending login request to Robinhood (check your phone for 2FA / SMS / push)...")
        login_res = r.login(username=username, password=password, expiresIn=2592000, store_session=True)
        if login_res:
            print("✅ Login successful! Session token cached on local machine.")
            data = sync_all_accounts()
        return login_res
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return None

def fetch_single_account(r, account_number, account_name):
    print(f"📊 Pulling live portfolio data for {account_name} ({account_number})...")
    port = r.request_get(f"https://api.robinhood.com/portfolios/{account_number}/")
    equity_nav = float(port.get('equity', 0.0))
    market_value = float(port.get('market_value', 0.0))
    cash = float(port.get('excess_margin', 0.0) or port.get('withdrawable_amount', 0.0) or 0.0)

    # 1. Fetch Stocks
    pos_res = r.request_get(f"https://api.robinhood.com/positions/?account_number={account_number}&nonzero=true")
    stocks = []
    symbols = []
    for p in pos_res.get('results', []):
        qty = float(p.get('quantity', 0.0))
        if qty <= 0:
            continue
        inst = r.get_instrument_by_url(p['instrument'])
        sym = inst['symbol']
        symbols.append(sym)
        stocks.append({
            'ticker': sym,
            'name': inst.get('simple_name') or inst.get('name') or sym,
            'shares': qty,
            'average_cost': float(p.get('average_buy_price', 0.0))
        })

    # Fetch live quotes
    if symbols:
        quotes = r.get_quotes(symbols)
        quote_map = {q['symbol']: q for q in quotes if q}
        for s in stocks:
            sym = s['ticker']
            q = quote_map.get(sym, {})
            price = float(q.get('last_trade_price') or q.get('last_extended_hours_trade_price') or 0.0)
            prev_close = float(q.get('previous_close') or price)
            s['price'] = price
            s['market_value'] = s['shares'] * price
            cost_total = s['shares'] * s['average_cost']
            s['cost_total'] = cost_total
            s['pnl'] = s['market_value'] - cost_total
            s['pnl_pct'] = (s['pnl'] / cost_total * 100) if cost_total > 0 else 0.0
            s['today_pct'] = ((price - prev_close) / prev_close * 100) if prev_close > 0 else 0.0
            s['pct_portfolio'] = (s['market_value'] / equity_nav * 100) if equity_nav > 0 else 0.0

    stocks.sort(key=lambda x: x['market_value'], reverse=True)

    # 2. Fetch Options
    opt_res = r.request_get(f"https://api.robinhood.com/options/positions/?account_number={account_number}&nonzero=true")
    options = []
    for o in opt_res.get('results', []):
        if account_number not in o.get('account', ''):
            continue
        qty = float(o.get('quantity', 0.0))
        if qty <= 0:
            continue
        opt_id = o.get('option_id')
        inst = r.get_option_instrument_data_by_id(opt_id)
        underlying = inst.get('chain_symbol')
        strike = float(inst.get('strike_price', 0.0))
        opt_type = inst.get('type')
        expiry = inst.get('expiration_date')

        q_list = r.get_option_market_data_by_id(opt_id)
        quote = q_list[0] if (q_list and isinstance(q_list, list)) else {}
        mark = float(quote.get('adjusted_mark_price', 0.0) or quote.get('mark_price', 0.0) or 0.0)
        avg_cost = float(o.get('average_price', 0.0)) / 100.0
        total_cost = avg_cost * qty * 100.0
        total_val = mark * qty * 100.0
        pnl = total_val - total_cost
        pnl_pct = (pnl / total_cost * 100) if total_cost > 0 else 0.0

        options.append({
            'underlying': underlying,
            'strike': strike,
            'type': opt_type.upper(),
            'direction': o.get('type', 'long'),
            'expiry': expiry,
            'quantity': qty,
            'mark': mark,
            'avg_cost': avg_cost,
            'total_value': total_val,
            'total_pnl': pnl,
            'total_pnl_pct': pnl_pct,
            'delta': quote.get('delta')
        })

    return {
        'account_number': account_number,
        'account_name': account_name,
        'equity_nav': equity_nav,
        'market_value': market_value,
        'cash': cash,
        'stocks': stocks,
        'options': options
    }

def sync_all_accounts():
    r = get_robinhood_client()
    try:
        r.login(expiresIn=86400*30)
    except Exception as e:
        print(f"⚠️ Error logging into Robinhood: {e}")
        return None

    # Fetch both accounts explicitly
    self_managed = fetch_single_account(r, '5PY51143', 'Self-Managed')
    agentic = fetch_single_account(r, '865935530', 'Agentic')

    combined = {
        'timestamp': datetime.now().isoformat(),
        'self_managed': self_managed,
        'agentic': agentic
    }

    state_path = "claude/robinhood-live-state.json"
    with open(state_path, "w") as f:
        json.dump(combined, f, indent=2)

    print("\n✅ Reconciled Both Accounts with Robinhood:")
    print(f"   [1] Self-Managed Account (5PY51143):")
    print(f"       Total Equity: ${self_managed['equity_nav']:,.2f}")
    print(f"       Stocks ({len(self_managed['stocks'])}): {', '.join(s['ticker'] for s in self_managed['stocks'])}")
    print(f"       Options ({len(self_managed['options'])}): {', '.join(o['underlying'] for o in self_managed['options'])}")

    print(f"   [2] Agentic Account (865935530):")
    print(f"       Total Equity: ${agentic['equity_nav']:,.2f} (Stocks: ${agentic['market_value']:,.2f}, Cash: ${agentic['cash']:,.2f})")
    print(f"       Stocks ({len(agentic['stocks'])}): {', '.join(s['ticker'] for s in agentic['stocks'])}")

    return combined

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'login':
        interactive_login()
    else:
        sync_all_accounts()
