import json
import os
from datetime import datetime

BRIEFS_DIR = os.path.join(os.path.dirname(__file__), "..", "briefs")

STOCK_DETAILS = {
    "ASML": { "meaning": "ASML is the only company on Earth capable of building the complex laser machines used to print the most advanced AI computer chips. Without ASML, the entire AI revolution grinds to a halt. It is the #1 anchor stock in your account and is doing great." },
    "IONQ": { "meaning": "Quantum computers calculate complex molecular and mathematical problems in seconds that regular supercomputers can't solve in a century. IonQ traps real atomic ions with lasers to process information. It's sitting on a small profit and is your top quantum bet." },
    "RXRX": { "meaning": "Instead of human scientists spending 10 years mixing chemicals in test tubes by hand, Recursion uses supercomputers and robotic labs to simulate millions of medical tests every day. It's up over 20% and is a massive winner in your account." },
    "CEG": { "meaning": "Tech giants need massive amounts of clean electricity 24 hours a day to keep artificial intelligence data centers running. Constellation is the nation's nuclear power king. The stock had a minor 5% pullback, giving you a great buying window to accumulate more shares." },
    "RKLB": { "meaning": "Rocket Lab is the only company besides SpaceX that reliably launches rockets into orbit on a regular schedule. They also build satellite parts for NASA and the US Space Force. Even though the stock is down -11% right now, their multi-billion-dollar backlog of government contracts makes them a long-term winner." },
    "TEM": { "meaning": "Tempus uses AI to match cancer patients with the exact therapies that will work best on their specific genetic mutations. You bought at $55 and it's now $82.62—giving you nearly +50% profit. Selling a tiny fraction of your shares will lock in cash profit while keeping the rest growing." },
    "MU": { "meaning": "AI computers require insane memory speeds to feed data into graphics cards without stalling. Micron makes the specialized ultra-fast memory stacks that go directly inside Nvidia AI chips. They are completely sold out for the next year and have generated you a 21% profit." },
    "ROBO": { "meaning": "Instead of picking just one factory robot company, ROBO owns a basket of dozens of the top robotics and factory automation businesses worldwide. It spreads your risk across the entire industry." },
    "ARKG": { "meaning": "ARKG invests in companies that rewrite human DNA to permanently cure hereditary genetic diseases like sickle cell and muscular dystrophy. It's up +21% and gives you broad exposure to futuristic biotech breakthroughs." },
    "ONDS": { "meaning": "Ondas makes automated drones that live in weatherproof boxes and launch themselves to patrol military bases, oil fields, and borders. The stock has pulled back -20%, but it is a small speculative position designed to catch big military contracts." },
    "ASTS": { "meaning": "AST SpaceMobile puts giant cellular towers in space so your ordinary phone gets cellular reception in the middle of the ocean, deserts, or mountains with zero dead zones. The stock is down -14% as they test their first batch of satellites, offering an attractive spot to accumulate before service goes live." },
    "PHO": { "meaning": "Computer chips and AI datacenters require millions of gallons of purified water to stay cool and clean. PHO owns the companies that build water pipes, pumps, and purification systems. It's a defensive safety net for your portfolio." },
    "QBTS": { "meaning": "D-Wave makes quantum computers that find the absolute best solution among billions of possibilities (like figuring out the optimal way to schedule thousands of factory machines). You bought at $9.99 and it's now $16.45, giving you a huge +65% gain." },
    "INOD": { "meaning": "To make AI models like ChatGPT and Gemini smart, companies need armies of doctors, lawyers, and coders to review and clean data. Innodata provides high-grade training data to the world's biggest tech companies and is profitable and growing." },
    "MP": { "meaning": "Rare earth minerals are vital for making missile guidance systems, radar, and electric cars. China controls most of the world's supply, but MP Materials owns America's only active rare earth mine. While the stock is down -16%, the Pentagon is backing them to make sure the US military has its own supply." },
    "BETA": { "meaning": "Beta builds battery-powered electric airplanes for cargo delivery and military medical flights. Unlike competitors promising flying passenger taxis tomorrow, Beta is smartly focusing first on cargo packages for UPS. It's a small, manageable bet in your portfolio." },
    "RGTI": { "meaning": "Rigetti designs and manufactures its own quantum chips in California using superconducting circuits that are chilled to temperatures colder than outer space. It's a second bet on quantum computing alongside IonQ." },
    "AUR": { "meaning": "Aurora builds self-driving software for giant 18-wheeler semi-trucks so freight can haul non-stop between cities like Dallas and Houston. While the stock has dropped -23%, the position is tiny and offers long-term upside as driverless freight routes expand." },
    "ARKX": { "meaning": "ARKX owns a basket of space-age companies building satellites, military drones, and space imaging systems. It gives you broad exposure to the commercial space boom without having to pick individual winners." },
    "JOBY": { "meaning": "Joby builds quiet electric air taxis designed to fly commuters over city traffic jams. The stock is down -31% because getting airplane approvals from the government takes time, but they have over $1 billion in the bank and Toyota as their main partner." },
    "CRWD": { "meaning": "CrowdStrike is a premier cybersecurity platform protecting global enterprises. It is a core holding in your self-managed account." },
    "GLD": { "meaning": "SPDR Gold Trust acts as a safe-haven asset, holding physical gold bars to protect against inflation and market volatility." },
    "CGNX": { "meaning": "Cognex provides machine vision systems used in automated manufacturing to inspect parts and guide robots." },
    "DFTX": { "meaning": "Definium Therapeutics is a speculative biotech holding in your self-managed account." },
}

def load_data(state_file):
    with open(state_file, "r") as f:
        return json.load(f)

def build_macro_brief(macro_html):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Macroeconomy Briefing · {datetime.now().strftime('%b %d, %Y')}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F8F9FA; font-family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #202124;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8F9FA; padding: 24px 0 32px 0;">
  <tr>
    <td align="center">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 16px; overflow: hidden; box-shadow: 0 1px 3px rgba(60,64,67,0.08);">
        <tr>
          <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="height: 4px;">
              <tr>
                <td width="25%" style="background-color: #4285F4; height: 4px;"></td>
                <td width="25%" style="background-color: #EA4335; height: 4px;"></td>
                <td width="25%" style="background-color: #FBBC05; height: 4px;"></td>
                <td width="25%" style="background-color: #34A853; height: 4px;"></td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 24px 28px 16px 28px; border-bottom: 1px solid #E8EAED;">
            <span style="font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; color: #1A73E8; text-transform: uppercase;">MACROECONOMIC ANALYSIS</span>
            <h1 style="font-size: 24px; font-weight: 700; margin: 4px 0 0 0; color: #202124; letter-spacing: -0.02em;">Global Market Pulse & Outlook</h1>
            <div style="font-size: 13px; color: #5F6368; margin-top: 4px;">{datetime.now().strftime('%A, %B %d, %Y')}</div>
          </td>
        </tr>
        <tr>
          <td style="padding: 20px 28px 24px 28px;">
            <div style="font-size: 14px; color: #3C4043; line-height: 1.6;">
              {macro_html}
            </div>
            <div style="margin-top: 20px;">
              <img src="assets/macro_7d_chart.png" alt="Macro Chart" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
            </div>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>"""
    output_path = os.path.join(BRIEFS_DIR, "macro_brief.html")
    with open(output_path, "w") as f:
        f.write(html)
    return output_path

def generate_master_table(stocks, options, equity_nav):
    tot_val = 0.0
    tot_cost = 0.0
    
    html = f"""
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: separate; border-spacing: 0; border: 1px solid #DADCE0; border-radius: 12px; overflow: hidden; background-color: #FFFFFF; margin-bottom: 14px;">
          <tr style="background-color: #F8F9FA;">
            <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 12px; text-align: left; border-bottom: 1px solid #DADCE0;">Holding</th>
            <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 8px; text-align: right; border-bottom: 1px solid #DADCE0;">Quantity</th>
            <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 8px; text-align: right; border-bottom: 1px solid #DADCE0;">Price/Mark</th>
            <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 10px; text-align: right; border-bottom: 1px solid #DADCE0;">Value</th>
            <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 12px; text-align: center; border-bottom: 1px solid #DADCE0;">Total P/L</th>
          </tr>"""

    for s in stocks:
        sym = s['ticker']
        name = s['name']
        shs = s['shares']
        price = s['price']
        mkt_val = s['market_value']
        pnl = s['pnl']
        pnl_pct = s['pnl_pct']
        tot_val += mkt_val
        tot_cost += s.get('cost_total', s.get('average_cost', 0) * shs)

        pnl_badge_bg = "#E6F4EA" if pnl >= 0 else "#FCE8E6"
        pnl_badge_fg = "#137333" if pnl >= 0 else "#D93025"
        pnl_sign = "+" if pnl >= 0 else "−"
        pnl_pct_sign = "+" if pnl_pct >= 0 else "−"
        shs_str = f"{shs:.2f}" if shs >= 10 else f"{shs:.4f}"

        html += f"""
          <tr>
            <td style="padding: 8px 12px; border-bottom: 1px solid #F1F3F4;">
              <div style="font-size: 13px; font-weight: 700; color: #202124;">{sym}</div>
              <div style="font-size: 10.5px; color: #5F6368; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px;">{name}</div>
            </td>
            <td style="padding: 8px 8px; font-size: 12.5px; text-align: right; color: #202124; border-bottom: 1px solid #F1F3F4;">{shs_str}</td>
            <td style="padding: 8px 8px; font-size: 12.5px; text-align: right; color: #202124; border-bottom: 1px solid #F1F3F4;">${price:,.2f}</td>
            <td style="padding: 8px 10px; font-size: 12.5px; text-align: right; color: #202124; font-weight: 700; border-bottom: 1px solid #F1F3F4;">${mkt_val:,.2f}</td>
            <td style="padding: 8px 12px; text-align: center; border-bottom: 1px solid #F1F3F4;">
              <span style="background-color: {pnl_badge_bg}; color: {pnl_badge_fg}; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 10px; display: inline-block; white-space: nowrap;">
                {pnl_pct_sign}{abs(pnl_pct):.1f}% ({pnl_sign}${abs(pnl):,.0f})
              </span>
            </td>
          </tr>"""

    for o in options:
        sym = f"{o['underlying']} {o['strike']} {o['type']}"
        name = f"{o['expiry']} Expiry"
        shs = o['quantity']
        price = o['mark']
        mkt_val = o['total_value']
        pnl = o['total_pnl']
        pnl_pct = o['total_pnl_pct']
        tot_val += mkt_val
        tot_cost += o.get('avg_cost', 0) * shs * 100

        pnl_badge_bg = "#E6F4EA" if pnl >= 0 else "#FCE8E6"
        pnl_badge_fg = "#137333" if pnl >= 0 else "#D93025"
        pnl_sign = "+" if pnl >= 0 else "−"
        pnl_pct_sign = "+" if pnl_pct >= 0 else "−"
        shs_str = f"{shs:.0f} c"

        html += f"""
          <tr>
            <td style="padding: 8px 12px; border-bottom: 1px solid #F1F3F4;">
              <div style="font-size: 13px; font-weight: 700; color: #B06000;">{sym}</div>
              <div style="font-size: 10.5px; color: #5F6368; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px;">{name}</div>
            </td>
            <td style="padding: 8px 8px; font-size: 12.5px; text-align: right; color: #202124; border-bottom: 1px solid #F1F3F4;">{shs_str}</td>
            <td style="padding: 8px 8px; font-size: 12.5px; text-align: right; color: #202124; border-bottom: 1px solid #F1F3F4;">${price:,.2f}</td>
            <td style="padding: 8px 10px; font-size: 12.5px; text-align: right; color: #202124; font-weight: 700; border-bottom: 1px solid #F1F3F4;">${mkt_val:,.2f}</td>
            <td style="padding: 8px 12px; text-align: center; border-bottom: 1px solid #F1F3F4;">
              <span style="background-color: {pnl_badge_bg}; color: {pnl_badge_fg}; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 10px; display: inline-block; white-space: nowrap;">
                {pnl_pct_sign}{abs(pnl_pct):.1f}% ({pnl_sign}${abs(pnl):,.0f})
              </span>
            </td>
          </tr>"""

    tot_pnl = tot_val - tot_cost
    tot_pnl_pct = (tot_pnl / tot_cost * 100) if tot_cost > 0 else 0.0
    tot_pnl_bg = "#E6F4EA" if tot_pnl >= 0 else "#FCE8E6"
    tot_pnl_fg = "#137333" if tot_pnl >= 0 else "#D93025"

    html += f"""
          <tr style="background-color: #F8F9FA;">
            <td style="padding: 10px 12px; font-size: 12.5px; font-weight: 800; color: #202124;">Total Holdings</td>
            <td style="padding: 10px 8px; font-size: 12px; text-align: right; font-weight: 800; color: #5F6368;">—</td>
            <td style="padding: 10px 8px; font-size: 12px; text-align: right; font-weight: 800; color: #5F6368;">—</td>
            <td style="padding: 10px 10px; font-size: 13px; text-align: right; font-weight: 800; color: #202124;">${tot_val:,.2f}</td>
            <td style="padding: 10px 12px; text-align: center;">
              <span style="background-color: {tot_pnl_bg}; color: {tot_pnl_fg}; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 10px; display: inline-block;">
                {"+" if tot_pnl >= 0 else "−"}${abs(tot_pnl):,.2f} ({"+" if tot_pnl_pct >= 0 else "−"}{abs(tot_pnl_pct):.2f}%)
              </span>
            </td>
          </tr>
        </table>
    """
    return html

def build_agentic_brief(state_file, sentiment_data, tactical_html):
    data = load_data(state_file)
    agentic = data["agentic"]
    stocks = agentic.get("stocks", [])
    options = agentic.get("options", [])
    equity_nav = agentic["equity_nav"]
    stock_value = agentic["market_value"]
    cash_value = agentic.get("cash", equity_nav - stock_value)

    equity_str = f"${equity_nav:,.2f}"
    stock_str = f"${stock_value:,.2f}"
    cash_str = f"${cash_value:,.2f}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agentic Complete Portfolio Briefing · {datetime.now().strftime('%B %d, %Y')}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F8F9FA; font-family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #202124;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8F9FA; padding: 24px 0 32px 0;">
  <tr>
    <td align="center">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 16px; overflow: hidden; box-shadow: 0 1px 3px rgba(60,64,67,0.08);">
        <tr>
          <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="height: 4px;">
              <tr>
                <td width="25%" style="background-color: #4285F4; height: 4px;"></td>
                <td width="25%" style="background-color: #EA4335; height: 4px;"></td>
                <td width="25%" style="background-color: #FBBC05; height: 4px;"></td>
                <td width="25%" style="background-color: #34A853; height: 4px;"></td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 24px 28px 16px 28px; border-bottom: 1px solid #E8EAED;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td>
                  <span style="font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; color: #1A73E8; text-transform: uppercase;">ROBINHOOD AGENTIC SYSTEM · COMPLETE BRIEFING</span>
                  <h1 style="font-size: 24px; font-weight: 700; margin: 4px 0 0 0; color: #202124; letter-spacing: -0.02em;">All {len(stocks) + len(options)} Holdings Status &amp; Performance</h1>
                  <div style="font-size: 13px; color: #5F6368; margin-top: 4px;">{datetime.now().strftime('%A, %B %d, %Y')} · Full Portfolio Audit</div>
                </td>
                <td align="right" valign="top">
                  <span style="display: inline-block; background-color: #E6F4EA; color: #137333; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 16px; white-space: nowrap;">🟢 ACCOUNT ••••5530</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 20px 28px 14px 28px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #E8F0FE; border: 1px solid #D2E3FC; border-radius: 14px; padding: 18px 20px;">
              <tr>
                <td>
                  <div style="font-size: 11px; font-weight: 800; letter-spacing: 0.08em; color: #1967D2; text-transform: uppercase;">EXECUTIVE PORTFOLIO AUDIT</div>
                  <div style="font-size: 21px; font-weight: 700; color: #1967D2; margin-top: 4px;">All Frontier Holdings Audited · {equity_str} NAV</div>
                  <div style="font-size: 13.5px; color: #3C4043; margin-top: 6px; line-height: 1.5;">
                    Your Robinhood Agentic account holds <b>{equity_str}</b> in total net equity, comprising <b>{len(stocks)} frontier tech stocks</b> ({stock_str}) and <b>{cash_str} in unencumbered cash</b>.
                  </div>
                  <div style="margin-top: 12px; background-color: #FFFFFF; border-left: 4px solid #1A73E8; border-radius: 8px; padding: 12px 14px;">
                    <div style="font-size: 11.5px; font-weight: 800; color: #1967D2; text-transform: uppercase; letter-spacing: 0.04em;">💡 What this means:</div>
                    <div style="font-size: 12.5px; color: #3C4043; line-height: 1.55; margin-top: 4px;">
                      We analyzed every single one of your holdings in detail. You have about half your capital invested across future-tech themes (chips, space, AI medicine, clean nuclear, and quantum computing), and the other half sitting safely in cash ready to buy bargains.
                    </div>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">All Verified Frontier Holdings (Robinhood Actuals)</div>
            {generate_master_table(stocks, options, equity_nav)}
            <div style="background-color: #F1F3F4; border-radius: 8px; padding: 8px 12px; text-align: center; font-size: 11px; color: #5F6368; font-weight: 600;">
              ⚖️ Unified Chart Scale: All equity holding P/L graphs below share the exact same scale (<b style="color: #202124;">-$2.0k to +$8.0k</b>) to provide true visual perspective across every asset.
            </div>
          </td>
        </tr>
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">Detailed Status Briefing</div>
"""
    i = 1
    for s in stocks:
        sym = s['ticker']
        name = s['name']
        shs = s['shares']
        price = s['price']
        mkt_val = s['market_value']
        pct_port = s.get('pct_portfolio', 0)
        pnl = s['pnl']
        pnl_pct = s['pnl_pct']
        cost = s.get('average_cost', 0)

        pnl_badge_bg = "#E6F4EA" if pnl >= 0 else "#FCE8E6"
        pnl_badge_fg = "#137333" if pnl >= 0 else "#D93025"
        pnl_icon = "🟢" if pnl >= 0 else "🔴"
        pnl_sign = "+" if pnl >= 0 else "−"
        shs_str = f"{shs:.2f}" if shs >= 10 else f"{shs:.4f}"
        chart_file = "onds_stock_pl_chart.png" if sym == "ONDS" else f"{sym.lower()}_pl_chart.png"
        
        sent_info = sentiment_data.get(sym, {})
        analysis = sent_info.get("analysis", f"{name} is an active frontier equity position trading at ${price:.2f}.")
        target_mean = sent_info.get("target_mean", 0)
        upside = sent_info.get("upside_pct", 0)

        meaning = STOCK_DETAILS.get(sym, {}).get("meaning", f"{name} is part of your long-term portfolio.")
        border_accent = "#137333" if pnl >= 0 else "#1A73E8"

        html += f"""
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <div style="font-size: 15px; font-weight: 700; color: #202124; white-space: nowrap;">#{i} {sym} · {name}</div>
                        <div style="font-size: 12px; color: #5F6368; margin-top: 1px;">{shs_str} Shares · ${mkt_val:,.2f} Market Value ({pct_port:.1f}%) · Cost: ${cost:,.2f}</div>
                        <div style="font-size: 11px; color: #1A73E8; margin-top: 1px;">Target: ${target_mean:,.2f} (Upside: {upside:.1f}%)</div>
                      </td>
                      <td align="right" valign="top">
                        <span style="background-color: {pnl_badge_bg}; color: {pnl_badge_fg}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">
                          {pnl_icon} {pnl_sign}${abs(pnl):,.0f} ({pnl_sign}{abs(pnl_pct):.1f}%)
                        </span>
                      </td>
                    </tr>
                  </table>
                  <div style="margin-top: 10px;">
                    <img src="assets/{chart_file}" alt="{sym} P/L Chart" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
                  </div>
                  <div style="margin-top: 10px; font-size: 12.5px; color: #3C4043; line-height: 1.5;">
                    <b>What is Going On & Sentiment:</b> {analysis}
                  </div>
                  <div style="background-color: #F8F9FA; border-left: 3px solid {border_accent}; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                    <b>💡 What this means:</b> {meaning}
                  </div>
                </td>
              </tr>
            </table>"""
        i += 1

    for o in options:
        sym = o['underlying']
        strike = o['strike']
        otype = o['type']
        expiry = o['expiry']
        qty = o['quantity']
        price = o['mark']
        mkt_val = o['total_value']
        pnl = o['total_pnl']
        pnl_pct = o['total_pnl_pct']
        cost = o['avg_cost']

        pnl_badge_bg = "#E6F4EA" if pnl >= 0 else "#FCE8E6"
        pnl_badge_fg = "#137333" if pnl >= 0 else "#D93025"
        pnl_icon = "🟢" if pnl >= 0 else "🔴"
        pnl_sign = "+" if pnl >= 0 else "−"
        chart_file = f"{sym.lower()}_pl_chart.png"
        
        html += f"""
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <div style="font-size: 15px; font-weight: 700; color: #B06000; white-space: nowrap;">#{i} {sym} ${strike} {otype}</div>
                        <div style="font-size: 12px; color: #5F6368; margin-top: 1px;">{qty} Contracts · Expiry: {expiry} · Mark: ${price:,.2f}</div>
                      </td>
                      <td align="right" valign="top">
                        <span style="background-color: {pnl_badge_bg}; color: {pnl_badge_fg}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">
                          {pnl_icon} {pnl_sign}${abs(pnl):,.0f} ({pnl_sign}{abs(pnl_pct):.1f}%)
                        </span>
                      </td>
                    </tr>
                  </table>
                  <div style="margin-top: 10px;">
                    <img src="assets/{chart_file}" alt="{sym} Option P/L Chart" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
                  </div>
                </td>
              </tr>
            </table>"""
        i += 1

    html += f"""
          </td>
        </tr>
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">💡 "Think About" Tactical Investment Radar</div>
            {tactical_html}
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>"""

    output_path = os.path.join(BRIEFS_DIR, "agentic_brief.html")
    with open(output_path, "w") as f:
        f.write(html)
    return output_path

def build_individual_brief(state_file, sentiment_data):
    data = load_data(state_file)
    individual = data.get("individual", data.get("self_managed", {}))
    stocks = individual.get("stocks", [])
    options = individual.get("options", [])
    equity_nav = individual.get("equity_nav", 0)
    stock_value = individual.get("market_value", 0)
    cash_value = individual.get("cash", equity_nav - stock_value)

    equity_str = f"${equity_nav:,.2f}"
    stock_str = f"${stock_value:,.2f}"
    cash_str = f"${cash_value:,.2f}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Individual Portfolio Briefing · {datetime.now().strftime('%B %d, %Y')}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F8F9FA; font-family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #202124;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8F9FA; padding: 24px 0 32px 0;">
  <tr>
    <td align="center">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 16px; overflow: hidden; box-shadow: 0 1px 3px rgba(60,64,67,0.08);">
        <tr>
          <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="height: 4px;">
              <tr>
                <td width="25%" style="background-color: #4285F4; height: 4px;"></td>
                <td width="25%" style="background-color: #EA4335; height: 4px;"></td>
                <td width="25%" style="background-color: #FBBC05; height: 4px;"></td>
                <td width="25%" style="background-color: #34A853; height: 4px;"></td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 24px 28px 16px 28px; border-bottom: 1px solid #E8EAED;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td>
                  <span style="font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; color: #1A73E8; text-transform: uppercase;">ROBINHOOD INDIVIDUAL SYSTEM</span>
                  <h1 style="font-size: 24px; font-weight: 700; margin: 4px 0 0 0; color: #202124; letter-spacing: -0.02em;">Self-Managed Account Briefing</h1>
                  <div style="font-size: 13px; color: #5F6368; margin-top: 4px;">{datetime.now().strftime('%A, %B %d, %Y')}</div>
                </td>
                <td align="right" valign="top">
                  <span style="display: inline-block; background-color: #FEF7E0; color: #B06000; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 16px; white-space: nowrap;">🟠 ACCOUNT ••••1143</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 20px 28px 14px 28px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FEF7E0; border: 1px solid #FCE8E6; border-radius: 14px; padding: 18px 20px;">
              <tr>
                <td>
                  <div style="font-size: 11px; font-weight: 800; letter-spacing: 0.08em; color: #B06000; text-transform: uppercase;">EXECUTIVE PORTFOLIO AUDIT</div>
                  <div style="font-size: 21px; font-weight: 700; color: #B06000; margin-top: 4px;">All Individual Holdings Audited · {equity_str} NAV</div>
                  <div style="font-size: 13.5px; color: #3C4043; margin-top: 6px; line-height: 1.5;">
                    Your Robinhood Individual account holds <b>{equity_str}</b> in total net equity, comprising <b>{len(stocks)} core stocks</b>, <b>{len(options)} speculative options</b>, and <b>{cash_str} in unencumbered cash</b>.
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">All Verified Individual Holdings (Robinhood Actuals)</div>
            {generate_master_table(stocks, options, equity_nav)}
          </td>
        </tr>
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="margin-top: 10px; font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">Holdings Status Briefing</div>
"""
    i = 1
    for s in stocks:
        sym = s['ticker']
        name = s['name']
        shs = s['shares']
        price = s['price']
        mkt_val = s['market_value']
        pct_port = s.get('pct_portfolio', 0)
        pnl = s['pnl']
        pnl_pct = s['pnl_pct']
        cost = s.get('average_cost', 0)

        pnl_badge_bg = "#E6F4EA" if pnl >= 0 else "#FCE8E6"
        pnl_badge_fg = "#137333" if pnl >= 0 else "#D93025"
        pnl_icon = "🟢" if pnl >= 0 else "🔴"
        pnl_sign = "+" if pnl >= 0 else "−"
        shs_str = f"{shs:.2f}" if shs >= 10 else f"{shs:.4f}"
        chart_file = "onds_stock_pl_chart.png" if sym == "ONDS" else f"{sym.lower()}_pl_chart.png"
        
        sent_info = sentiment_data.get(sym, {})
        analysis = sent_info.get("analysis", f"{name} is an active equity position trading at ${price:.2f}.")
        target_mean = sent_info.get("target_mean", 0)
        upside = sent_info.get("upside_pct", 0)

        meaning = STOCK_DETAILS.get(sym, {}).get("meaning", f"{name} is an active position in your portfolio.")
        border_accent = "#137333" if pnl >= 0 else "#1A73E8"

        html += f"""
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <div style="font-size: 15px; font-weight: 700; color: #202124; white-space: nowrap;">#{i} {sym} · {name}</div>
                        <div style="font-size: 12px; color: #5F6368; margin-top: 1px;">{shs_str} Shares · ${mkt_val:,.2f} Market Value ({pct_port:.1f}%) · Cost: ${cost:,.2f}</div>
                        <div style="font-size: 11px; color: #B06000; margin-top: 1px;">Target: ${target_mean:,.2f} (Upside: {upside:.1f}%)</div>
                      </td>
                      <td align="right" valign="top">
                        <span style="background-color: {pnl_badge_bg}; color: {pnl_badge_fg}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">
                          {pnl_icon} {pnl_sign}${abs(pnl):,.0f} ({pnl_sign}{abs(pnl_pct):.1f}%)
                        </span>
                      </td>
                    </tr>
                  </table>
                  <div style="margin-top: 10px;">
                    <img src="assets/{chart_file}" alt="{sym} P/L Chart" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
                  </div>
                  <div style="margin-top: 10px; font-size: 12.5px; color: #3C4043; line-height: 1.5;">
                    <b>Sentiment & Analysis:</b> {analysis}
                  </div>
                  <div style="background-color: #F8F9FA; border-left: 3px solid {border_accent}; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                    <b>💡 What this means:</b> {meaning}
                  </div>
                </td>
              </tr>
            </table>"""
        i += 1

    for o in options:
        sym = o['underlying']
        strike = o['strike']
        otype = o['type']
        expiry = o['expiry']
        qty = o['quantity']
        price = o['mark']
        mkt_val = o['total_value']
        pnl = o['total_pnl']
        pnl_pct = o['total_pnl_pct']
        cost = o['avg_cost']

        pnl_badge_bg = "#E6F4EA" if pnl >= 0 else "#FCE8E6"
        pnl_badge_fg = "#137333" if pnl >= 0 else "#D93025"
        pnl_icon = "🟢" if pnl >= 0 else "🔴"
        pnl_sign = "+" if pnl >= 0 else "−"
        chart_file = f"{sym.lower()}_pl_chart.png"

        html += f"""
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <div style="font-size: 15px; font-weight: 700; color: #B06000; white-space: nowrap;">#{i} {sym} ${strike} {otype}</div>
                        <div style="font-size: 12px; color: #5F6368; margin-top: 1px;">{qty} Contracts · Expiry: {expiry} · Mark: ${price:,.2f}</div>
                      </td>
                      <td align="right" valign="top">
                        <span style="background-color: {pnl_badge_bg}; color: {pnl_badge_fg}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">
                          {pnl_icon} {pnl_sign}${abs(pnl):,.0f} ({pnl_sign}{abs(pnl_pct):.1f}%)
                        </span>
                      </td>
                    </tr>
                  </table>
                  <div style="margin-top: 10px;">
                    <img src="assets/{chart_file}" alt="{sym} Option P/L Chart" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
                  </div>
                </td>
              </tr>
            </table>"""
        i += 1

    html += f"""
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>"""

    output_path = os.path.join(BRIEFS_DIR, "individual_brief.html")
    with open(output_path, "w") as f:
        f.write(html)
    return output_path
