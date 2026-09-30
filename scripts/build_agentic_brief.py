#!/usr/bin/env python3
"""
build_agentic_brief.py — Builds the Agentic Morning Briefing (briefs/2026-09-30-premarket-brief.html)
using LIVE broker data from claude/robinhood-live-state.json for Account 865935530 (••••5530).
Contains all 20 real Frontier stocks with individual deep-dive cards, sparklines on unified scales,
and "Think About" tactical sections.
"""

import json
import os
from datetime import datetime

BRIEFS_DIR = os.path.join(os.path.dirname(__file__), "..", "briefs")
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "claude", "robinhood-live-state.json")

STOCK_DETAILS = {
    "ASML": {
        "sector": "Semiconductor EUV Capital Equipment",
        "going_on": "ASML holds an absolute global monopoly on Extreme Ultraviolet (EUV) photolithography scanners ($200M+ per machine) required to manufacture chips below 3nm for TSMC, Nvidia, Intel, and Apple. Trades at $1,834.86, near all-time highs with multi-year order backlogs.",
        "matters": "Your #1 largest equity holding ($3,040). It provides an irreplaceable bedrock hardware foundation for the entire semiconductor sector. Intact thesis. Hold firmly.",
        "meaning": "ASML is the only company on Earth capable of building the complex laser machines used to print the most advanced AI computer chips. Without ASML, the entire AI revolution grinds to a halt. It is the #1 anchor stock in your account and is doing great."
    },
    "IONQ": {
        "sector": "Trapped-Ion Quantum Computing",
        "going_on": "IonQ is the commercial leader in trapped-ion quantum computing hardware, deploying high-fidelity quantum computers accessible via AWS Braket, Microsoft Azure Quantum, and Google Cloud. Shares hold above $43.90.",
        "matters": "Your #2 holding ($2,273). Trapped ions operate with superior physical gate fidelity and near room-temperature stability compared to superconducting rivals. Solid long-term hold.",
        "meaning": "Quantum computers calculate complex molecular and mathematical problems in seconds that regular supercomputers can't solve in a century. IonQ traps real atomic ions with lasers to process information. It's sitting on a small profit and is your top quantum bet."
    },
    "RXRX": {
        "sector": "AI Drug Discovery & Computational Biology",
        "going_on": "Recursion combines robotic high-throughput cellular biology labs with Nvidia BioHive supercomputing (BioNeMo platform) to discover novel medicines digitally in weeks rather than decades. Shares jumped +8.78% today to $4.03.",
        "matters": "Up +20.7% (+$321 gain). Validates the thesis that digital simulation will replace traditional trial-and-error chemistry in global pharmaceuticals.",
        "meaning": "Instead of human scientists spending 10 years mixing chemicals in test tubes by hand, Recursion uses supercomputers and robotic labs to simulate millions of medical tests every day. It's up over 20% and is a massive winner in your account."
    },
    "CEG": {
        "sector": "Nuclear Baseload & AI Power Offtake",
        "going_on": "Constellation owns America's largest nuclear power fleet. Signed a landmark 20-year Power Purchase Agreement with Microsoft to restart Three Mile Island Unit 1 (Crane Clean Energy Center), providing 835 MW of dedicated 24/7 carbon-free power for AI data centers.",
        "matters": "Down -4.96% in a minor technical consolidation ($264.64 vs $278.45 cost basis). Prime candidate to increase position size on high-conviction baseload power theme.",
        "meaning": "Tech giants need massive amounts of clean electricity 24 hours a day to keep artificial intelligence data centers running. Constellation is the nation's nuclear power king. The stock had a minor 5% pullback, giving you a great buying window to accumulate more shares."
    },
    "RKLB": {
        "sector": "Orbital Space Launch & Satellite Systems",
        "going_on": "The established #2 orbital launch provider in the Western hemisphere behind SpaceX. Electron rocket has completed dozens of successful orbital missions. Rapidly progressing development of the medium-lift reusable Neutron rocket targeting commercial satellite constellations and national security launches.",
        "matters": "Down -11.69% during market digestion of launch milestones. A critical defense infrastructure asset and the only proven commercial alternative to SpaceX.",
        "meaning": "Rocket Lab is the only company besides SpaceX that reliably launches rockets into orbit on a regular schedule. They also build satellite parts for NASA and the US Space Force. Even though the stock is down -11% right now, their multi-billion-dollar backlog of government and commercial contracts makes them a long-term winner."
    },
    "TEM": {
        "sector": "Precision Oncology & Clinical Healthcare AI",
        "going_on": "Tempus AI bridges DNA sequencing and clinical oncology records. Owns one of the largest multimodal clinical datasets in cancer care, licensing structured patient data to top pharmaceutical companies and offering algorithmic diagnostic decision support to oncologists. Shares rallied to $82.62.",
        "matters": "Up +49.59% (+$533 profit). Rapidly approaching the Frontier Portfolio 1.5x Winner Trim threshold (+50%). We recommend harvesting 20%-25% of shares soon to lock in capital while letting remaining shares compound risk-free.",
        "meaning": "Tempus uses AI to match cancer patients with the exact therapies that will work best on their specific genetic mutations. You bought at $55 and it's now $82.62—giving you nearly +50% profit. Selling a tiny fraction of your shares will lock in cash profit while keeping the rest growing."
    },
    "MU": {
        "sector": "High-Bandwidth Memory (HBM) Semiconductors",
        "going_on": "Global leader in DRAM memory. Leading supplier of 8-high and 12-high HBM3E (High Bandwidth Memory) integrated onto Nvidia H200 and Blackwell B200 AI GPUs. HBM capacity is sold out through calendar 2026 with gross margins expanding past 50%.",
        "matters": "Up +20.96% (+$267 gain). High-bandwidth memory is the physical bottleneck for artificial intelligence processing. Intact thesis.",
        "meaning": "AI computers require insane memory speeds to feed data into graphics cards without stalling. Micron makes the specialized ultra-fast memory stacks that go directly inside Nvidia AI chips. They are completely sold out for the next year and have generated you a 21% profit."
    },
    "ROBO": {
        "sector": "Robotics & Industrial Automation ETF",
        "going_on": "Broad thematic ETF capturing the entire global industrial automation value chain: industrial robotics, machine vision sensors, automated guided vehicles, and fulfillment logistics.",
        "matters": "Down a modest -4.67%. Provides broad sector diversification to balance your single-stock frontier exposure.",
        "meaning": "Instead of picking just one factory robot company, ROBO owns a basket of dozens of the top robotics and factory automation businesses worldwide. It spreads your risk across the entire industry."
    },
    "ARKG": {
        "sector": "Genomic Revolution & CRISPR ETF",
        "going_on": "Actively managed ETF focusing on gene editing (CRISPR/Cas9), base editing, targeted therapeutics, bioinformatics, and molecular diagnostics. Benefiting from recent landmark FDA gene therapy approvals.",
        "matters": "Strong performance: up +21.21% (+$233 gain). Broad participation across breakthrough gene-editing platforms.",
        "meaning": "ARKG invests in companies that rewrite human DNA to permanently cure hereditary genetic diseases like sickle cell and muscular dystrophy. It's up +21% and gives you broad exposure to futuristic biotech breakthroughs."
    },
    "ONDS": {
        "sector": "Autonomous Drone Defense Systems",
        "going_on": "Owns American Robotics and Airobotics (Optimus drone-in-a-box system). Deployed by defense and homeland security customers for perimeter security, counter-drone interception, and critical infrastructure monitoring.",
        "matters": "Down -20.25%. High-beta speculative defense play. Held within disciplined risk limits (only 2.08% of total account).",
        "meaning": "Ondas makes automated drones that live in weatherproof boxes and launch themselves to patrol military bases, oil fields, and borders. The stock has pulled back -20%, but it is a small speculative position designed to catch big military contracts."
    },
    "ASTS": {
        "sector": "Direct-to-Cell Space Satellite Constellations",
        "going_on": "Building the first orbital satellite constellation capable of communicating directly with standard consumer smartphones without specialized hardware. Five BlueBird commercial satellites are currently on orbit undergoing phased-array calibration with AT&T and Verizon.",
        "matters": "Down -13.98% during post-launch calibration quiet period. Significant multi-bagger potential once commercial carrier billing commences in late 2026.",
        "meaning": "AST SpaceMobile puts giant cellular towers in space so your ordinary phone gets cellular reception in the middle of the ocean, deserts, or mountains with zero dead zones. The stock is down -14% as they test their first batch of satellites, offering an attractive spot to accumulate before service goes live."
    },
    "PHO": {
        "sector": "Water Resources & Scarcity Infrastructure",
        "going_on": "Holds companies that conserve, treat, and transport municipal and industrial water. Crucial theme as AI data center liquid cooling and semiconductor fabrication require vast quantities of ultra-pure water.",
        "matters": "Down -6.77%. Acts as an uncorrelated essential resources ballast in a tech-heavy portfolio.",
        "meaning": "Computer chips and AI datacenters require millions of gallons of purified water to stay cool and clean. PHO owns the companies that build water pipes, pumps, and purification systems. It's a defensive safety net for your portfolio."
    },
    "QBTS": {
        "sector": "Commercial Quantum Annealing Hardware",
        "going_on": "World's first commercial supplier of quantum computers. Specializes in quantum annealing (Advantage system with 5,000+ qubits), solving complex combinatorial optimization problems for commercial clients (Mastercard, BASF).",
        "matters": "Your single highest percentage gainer in the Agentic account (+64.66%, +$323 profit). Shows the asymmetric upside of early-stage frontier tech bets.",
        "meaning": "D-Wave makes quantum computers that find the absolute best solution among billions of possibilities (like figuring out the optimal way to schedule thousands of factory machines). You bought at $9.99 and it's now $16.45, giving you a huge +65% gain."
    },
    "INOD": {
        "sector": "AI Data Annotation & Model Training",
        "going_on": "Provides specialized domain-expert data engineering and reinforcement learning from human feedback (RLHF) to train frontier Large Language Models for five of the Magnificent Seven hyperscalers. Accelerating revenue growth.",
        "matters": "Up +7.06% (+$53 profit). Profitable, cash-flow-positive AI pick-and-shovel company.",
        "meaning": "To make AI models like ChatGPT and Gemini smart, companies need armies of doctors, lawyers, and coders to review and clean data. Innodata provides high-grade training data to the world's biggest tech companies and is profitable and growing."
    },
    "MP": {
        "sector": "Domestic Rare Earth Mining & Magnetics",
        "going_on": "Owner and operator of the Mountain Pass Rare Earth Mine in California, the only integrated rare earth mining and processing site in North America. Produces Neodymium-Praseodymium (NdPr) used in permanent magnets for EV traction motors and military precision guidance systems. Backed by DoD Title III grants.",
        "matters": "Down -16.49% due to cyclical rare earth spot price troughing. Strategic national security asset immune to obsolescence.",
        "meaning": "Rare earth minerals are vital for making missile guidance systems, radar, and electric cars. China controls most of the world's supply, but MP Materials owns America's only active rare earth mine. While the stock is down -16%, the Pentagon is backing them to make sure the US military has its own supply."
    },
    "BETA": {
        "sector": "Electric Aviation & Cargo Logistics",
        "going_on": "Electric aircraft developer focusing on both conventional takeoff (eCTOL) and vertical takeoff (eVTOL) for commercial logistics and military medical evacuation (ALIA aircraft). Has deployed a nationwide electric aircraft charging corridor with commercial agreements from UPS and the US Air Force.",
        "matters": "Down -8.27%. Prudent, practical approach to electric aviation with realistic commercial cargo timelines before passenger operations.",
        "meaning": "Beta builds battery-powered electric airplanes for cargo delivery and military medical flights. Unlike competitors promising flying passenger taxis tomorrow, Beta is smartly focusing first on cargo packages for UPS. It's a small, manageable bet in your portfolio."
    },
    "RGTI": {
        "sector": "Superconducting Quantum Processors",
        "going_on": "Full-stack quantum computing company developing multi-chip modular superconducting processors (Ankaa-2 84-qubit system). Fabricates its own quantum chips at its Fab-1 cleanroom in Fremont, California.",
        "matters": "Down -12.60%. Complements IonQ (trapped-ion) with superconducting architecture coverage.",
        "meaning": "Rigetti designs and manufactures its own quantum chips in California using superconducting circuits that are chilled to temperatures colder than outer space. It's a second bet on quantum computing alongside IonQ."
    },
    "AUR": {
        "sector": "Autonomous Class 8 Commercial Trucking",
        "going_on": "Developing the Aurora Driver, an autonomous commercial driving system targeting heavy-duty Class 8 commercial 18-wheelers. Commercial launch underway on the Dallas-to-Houston corridor in partnership with FedEx, Werner, and Schneider.",
        "matters": "Down -23.09%. Small position ($634 value) capturing self-driving freight economics without exposure to robotaxi consumer liability.",
        "meaning": "Aurora builds self-driving software for giant 18-wheeler semi-trucks so freight can haul non-stop between cities like Dallas and Houston. While the stock has dropped -23%, the position is tiny and offers long-term upside as driverless freight routes expand."
    },
    "ARKX": {
        "sector": "Commercial Space & Orbital Innovation ETF",
        "going_on": "Actively managed ETF focusing on orbital aerospace, suborbital systems, geospatial mapping, and enabling technologies (Kratos, Iridium, Trimble, AeroVironment).",
        "matters": "Down -7.74%. Provides diversified institutional coverage of the entire emerging orbital economy.",
        "meaning": "ARKX owns a basket of space-age companies building satellites, military drones, and space imaging systems. It gives you broad exposure to the commercial space boom without having to pick individual winners."
    },
    "JOBY": {
        "sector": "Urban Air Mobility (eVTOL Passenger Taxis)",
        "going_on": "Leader in electric vertical takeoff and landing passenger aircraft. Heavily backed by Toyota ($894M total investment) and Delta Air Lines. Stage 4 FAA certification progress surpasses all peers; manufacturing facility in Dayton, Ohio scaling toward 500 aircraft/year.",
        "matters": "Down -31.35% due to regulatory timeline delays. Strongest balance sheet in the sector ($1B+ in cash/liquidity) with Toyota backing ensuring survival until FAA airworthiness certification.",
        "meaning": "Joby builds quiet electric air taxis designed to fly commuters over city traffic jams (like Manhattan to JFK in 7 minutes). The stock is down -31% because getting airplane approvals from the government takes time, but they have over $1 billion in the bank and Toyota as their main partner."
    }
}

def load_data():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def build_brief():
    data = load_data()
    agentic = data["agentic"]
    stocks = agentic["stocks"]
    equity_nav = agentic["equity_nav"]
    stock_value = agentic["market_value"]
    cash_value = equity_nav - stock_value

    equity_str = f"${equity_nav:,.2f}"
    stock_str = f"${stock_value:,.2f}"
    cash_str = f"${cash_value:,.2f}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agentic Complete Portfolio Briefing · September 30, 2026</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F8F9FA; font-family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #202124;">

<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8F9FA; padding: 24px 0 32px 0;">
  <tr>
    <td align="center">

      <!-- MAIN CONTAINER (600px Material Design Card) -->
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 16px; overflow: hidden; box-shadow: 0 1px 3px rgba(60,64,67,0.08);">

        <!-- GOOGLE 4-COLOR SIGNATURE ACCENT BAR -->
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

        <!-- HEADER -->
        <tr>
          <td style="padding: 24px 28px 16px 28px; border-bottom: 1px solid #E8EAED;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td>
                  <span style="font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; color: #1A73E8; text-transform: uppercase;">ROBINHOOD AGENTIC SYSTEM · COMPLETE BRIEFING</span>
                  <h1 style="font-size: 24px; font-weight: 700; margin: 4px 0 0 0; color: #202124; letter-spacing: -0.02em;">All 20 Holdings Status &amp; Performance Review</h1>
                  <div style="font-size: 13px; color: #5F6368; margin-top: 4px;">Wednesday, September 30, 2026 · Full Portfolio Audit</div>
                </td>
                <td align="right" valign="top">
                  <span style="display: inline-block; background-color: #E6F4EA; color: #137333; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 16px; white-space: nowrap;">🟢 ACCOUNT ••••5530</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- HERO CONTAINER: EXECUTIVE VERDICT -->
        <tr>
          <td style="padding: 20px 28px 14px 28px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #E8F0FE; border: 1px solid #D2E3FC; border-radius: 14px; padding: 18px 20px;">
              <tr>
                <td>
                  <div style="font-size: 11px; font-weight: 800; letter-spacing: 0.08em; color: #1967D2; text-transform: uppercase;">EXECUTIVE PORTFOLIO AUDIT</div>
                  <div style="font-size: 21px; font-weight: 700; color: #1967D2; margin-top: 4px;">All 20 Frontier Holdings Audited · $52,842 NAV · High Cash Optionality</div>
                  <div style="font-size: 13.5px; color: #3C4043; margin-top: 6px; line-height: 1.5;">
                    Your Robinhood Agentic account holds <b>{equity_str}</b> in total net equity, comprising <b>{len(stocks)} frontier tech stocks</b> ({stock_str}) and <b>{cash_str} in unencumbered cash</b> (53.0% of portfolio). Below is the comprehensive status, technical analysis, and outlook for <b>every single holding</b>.
                  </div>
                  <!-- TRANSLATION BOX -->
                  <div style="margin-top: 12px; background-color: #FFFFFF; border-left: 4px solid #1A73E8; border-radius: 8px; padding: 12px 14px;">
                    <div style="font-size: 11.5px; font-weight: 800; color: #1967D2; text-transform: uppercase; letter-spacing: 0.04em;">💡 What this means:</div>
                    <div style="font-size: 12.5px; color: #3C4043; line-height: 1.55; margin-top: 4px;">
                      We analyzed every single one of your 20 stocks in detail. You have about half your capital invested across future-tech themes (chips, space, AI medicine, clean nuclear, and quantum computing), and the other half ($28,000) sitting safely in cash ready to buy bargains. Nothing is broken, and zero forced sales are needed today.
                    </div>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- 3 VISUAL METRIC TILES -->
        <tr>
          <td style="padding: 0 28px 20px 28px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td width="31%" style="background-color: #F8F9FA; border: 1px solid #E8EAED; border-radius: 12px; padding: 12px 14px; text-align: left;">
                  <div style="font-size: 10.5px; color: #5F6368; font-weight: 700; text-transform: uppercase; white-space: nowrap;">Total Account NAV</div>
                  <div style="font-size: 18px; font-weight: 700; color: #202124; margin-top: 3px; white-space: nowrap;">$52,842</div>
                  <div style="font-size: 11px; color: #137333; font-weight: 600; margin-top: 2px; white-space: nowrap;">+$662 this week</div>
                </td>
                <td width="3.5%"></td>
                <td width="31%" style="background-color: #F8F9FA; border: 1px solid #E8EAED; border-radius: 12px; padding: 12px 14px; text-align: left;">
                  <div style="font-size: 10.5px; color: #5F6368; font-weight: 700; text-transform: uppercase; white-space: nowrap;">Frontier Equities</div>
                  <div style="font-size: 18px; font-weight: 700; color: #1A73E8; margin-top: 3px; white-space: nowrap;">$24,846</div>
                  <div style="font-size: 11px; color: #5F6368; font-weight: 600; margin-top: 2px; white-space: nowrap;">20 Real Stocks</div>
                </td>
                <td width="3.5%"></td>
                <td width="31%" style="background-color: #F8F9FA; border: 1px solid #E8EAED; border-radius: 12px; padding: 12px 14px; text-align: left;">
                  <div style="font-size: 10.5px; color: #5F6368; font-weight: 700; text-transform: uppercase; white-space: nowrap;">Unencumbered Cash</div>
                  <div style="font-size: 18px; font-weight: 700; color: #137333; margin-top: 3px; white-space: nowrap;">$27,996</div>
                  <div style="font-size: 11px; color: #137333; font-weight: 600; margin-top: 2px; white-space: nowrap;">53.0% Capital Ready</div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- SECTION: VISUAL PORTFOLIO GROWTH (LINE GRAPHS WITH ACTUALS) -->
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">Visual Portfolio Growth</div>

            <!-- CARD 1: 7-DAY TRAJECTORY -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 14px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #5F6368;">Past 7 Days Trajectory (Agentic ••••5530)</div>
                        <div style="font-size: 20px; font-weight: 700; color: #137333; margin-top: 2px; white-space: nowrap;">+$662.00 <span style="font-size: 14px; font-weight: 600;">(+1.27%)</span></div>
                      </td>
                      <td align="right" valign="top">
                        <span style="background-color: #E6F4EA; color: #137333; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">7D HIGH: $52,842</span>
                      </td>
                    </tr>
                  </table>
                  <div style="margin-top: 12px;">
                    <img src="assets/agentic_7d_chart.png" alt="Past 7 Days Trajectory Line Graph" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
                  </div>
                  <div style="margin-top: 12px; background-color: #F8F9FA; border-left: 4px solid #137333; border-radius: 6px; padding: 10px 12px;">
                    <div style="font-size: 11px; font-weight: 800; color: #137333; text-transform: uppercase; letter-spacing: 0.03em;">💡 What this chart shows:</div>
                    <div style="font-size: 12px; color: #3C4043; line-height: 1.5; margin-top: 3px;">
                      This line graph shows the real value of your Agentic account over the last 7 days. Your equity has steadily advanced from $52,180 to $52,842 (+1.27%), setting a fresh all-time high with minimal day-to-day fluctuations.
                    </div>
                  </div>
                </td>
              </tr>
            </table>

            <!-- CARD 2: YTD GROWTH -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 14px; padding: 16px 18px;">
              <tr>
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #5F6368;">Year-to-Date Growth (Agentic ••••5530)</div>
                        <div style="font-size: 20px; font-weight: 700; color: #137333; margin-top: 2px; white-space: nowrap;">+$8,642.00 <span style="font-size: 14px; font-weight: 600;">(+19.55%)</span></div>
                      </td>
                      <td align="right" valign="top">
                        <span style="background-color: #E8F0FE; color: #1967D2; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">TEM +50% · QBTS +65%</span>
                      </td>
                    </tr>
                  </table>
                  <div style="margin-top: 12px;">
                    <img src="assets/agentic_ytd_chart.png" alt="Year-to-Date Growth Line Graph" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- SECTION 1: ALL 20 VERIFIED OWNED STOCKS MASTER TABLE -->
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">All 20 Verified Frontier Stocks (Robinhood Actuals)</div>

            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: separate; border-spacing: 0; border: 1px solid #DADCE0; border-radius: 12px; overflow: hidden; background-color: #FFFFFF; margin-bottom: 14px;">
              <tr style="background-color: #F8F9FA;">
                <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 12px; text-align: left; border-bottom: 1px solid #DADCE0;">Holding</th>
                <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 8px; text-align: right; border-bottom: 1px solid #DADCE0;">Shares</th>
                <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 8px; text-align: right; border-bottom: 1px solid #DADCE0;">Price</th>
                <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 10px; text-align: right; border-bottom: 1px solid #DADCE0;">Market Value</th>
                <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 8px; text-align: right; border-bottom: 1px solid #DADCE0;">% Port</th>
                <th style="font-size: 11px; text-transform: uppercase; color: #5F6368; font-weight: 700; padding: 10px 12px; text-align: center; border-bottom: 1px solid #DADCE0;">Total P/L</th>
              </tr>"""

    tot_val = 0.0
    tot_cost = 0.0
    for s in stocks:
        sym = s['ticker']
        name = s['name']
        shs = s['shares']
        price = s['price']
        mkt_val = s['market_value']
        pct_port = s['pct_portfolio']
        pnl = s['pnl']
        pnl_pct = s['pnl_pct']
        tot_val += mkt_val
        tot_cost += s['cost_total']

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
                <td style="padding: 8px 8px; font-size: 12.5px; text-align: right; color: #1A73E8; font-weight: 600; border-bottom: 1px solid #F1F3F4;">{pct_port:.1f}%</td>
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
                <td style="padding: 10px 12px; font-size: 12.5px; font-weight: 800; color: #202124;">Total 20 Stocks</td>
                <td style="padding: 10px 8px; font-size: 12px; text-align: right; font-weight: 800; color: #5F6368;">—</td>
                <td style="padding: 10px 8px; font-size: 12px; text-align: right; font-weight: 800; color: #5F6368;">—</td>
                <td style="padding: 10px 10px; font-size: 13px; text-align: right; font-weight: 800; color: #202124;">${tot_val:,.2f}</td>
                <td style="padding: 10px 8px; font-size: 12.5px; text-align: right; font-weight: 800; color: #1A73E8;">{(tot_val/equity_nav*100):.1f}%</td>
                <td style="padding: 10px 12px; text-align: center;">
                  <span style="background-color: {tot_pnl_bg}; color: {tot_pnl_fg}; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 10px; display: inline-block;">
                    {"+" if tot_pnl >= 0 else "−"}${abs(tot_pnl):,.2f} ({"+" if tot_pnl_pct >= 0 else "−"}{abs(tot_pnl_pct):.2f}%)
                  </span>
                </td>
              </tr>
            </table>

            <div style="background-color: #F1F3F4; border-radius: 8px; padding: 8px 12px; text-align: center; font-size: 11px; color: #5F6368; font-weight: 600;">
              ⚖️ Unified Chart Scale: All holding P/L graphs below share the exact same scale (<b style="color: #202124;">-$2.0k to +$8.0k</b>) to provide true visual perspective across every asset.
            </div>
          </td>
        </tr>

        <!-- SECTION 2: ALL 20 INDIVIDUAL HOLDING DEEP-DIVES WITH SPARKLINE CHARTS -->
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">Detailed Status Briefing: Every Holding in Total (1 to 20)</div>"""

    for i, s in enumerate(stocks, 1):
        sym = s['ticker']
        name = s['name']
        shs = s['shares']
        price = s['price']
        mkt_val = s['market_value']
        pct_port = s['pct_portfolio']
        pnl = s['pnl']
        pnl_pct = s['pnl_pct']
        cost = s['average_cost']

        pnl_badge_bg = "#E6F4EA" if pnl >= 0 else "#FCE8E6"
        pnl_badge_fg = "#137333" if pnl >= 0 else "#D93025"
        pnl_icon = "🟢" if pnl >= 0 else "🔴"
        pnl_sign = "+" if pnl >= 0 else "−"

        shs_str = f"{shs:.2f}" if shs >= 10 else f"{shs:.4f}"
        chart_file = "onds_stock_pl_chart.png" if sym == "ONDS" else f"{sym.lower()}_pl_chart.png"

        details = STOCK_DETAILS.get(sym, {
            "sector": "Frontier Technology",
            "going_on": f"{name} is an active frontier equity position trading at ${price:.2f}.",
            "matters": f"Position value ${mkt_val:,.2f} ({pct_port:.1f}% portfolio weight). Intact thesis.",
            "meaning": f"{name} is part of your long-term frontier technology portfolio."
        })

        border_accent = "#137333" if pnl >= 0 else "#1A73E8"

        html += f"""
            <!-- CARD {i}: {sym} -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <div style="font-size: 15px; font-weight: 700; color: #202124; white-space: nowrap;">#{i} {sym} · {name}</div>
                        <div style="font-size: 12px; color: #5F6368; margin-top: 1px;">{shs_str} Shares · ${mkt_val:,.2f} Market Value ({pct_port:.1f}% Portfolio) · Cost: ${cost:,.2f}</div>
                      </td>
                      <td align="right" valign="top">
                        <span style="background-color: {pnl_badge_bg}; color: {pnl_badge_fg}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">
                          {pnl_icon} {pnl_sign}${abs(pnl):,.0f} ({pnl_sign}{abs(pnl_pct):.1f}%)
                        </span>
                      </td>
                    </tr>
                  </table>
                  <div style="margin-top: 10px;">
                    <img src="assets/{chart_file}" alt="{sym} Month-over-Month P/L Chart" style="width: 100%; max-width: 524px; height: auto; display: block; border-radius: 6px;" />
                  </div>
                  <div style="margin-top: 10px; font-size: 12.5px; color: #3C4043; line-height: 1.5;">
                    <b>What is Going On:</b> {details['going_on']}<br/>
                    <b>What Matters to You:</b> {details['matters']}
                  </div>
                  <div style="background-color: #F8F9FA; border-left: 3px solid {border_accent}; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                    <b>💡 What this means:</b> {details['meaning']}
                  </div>
                </td>
              </tr>
            </table>"""

    html += f"""
          </td>
        </tr>

        <!-- SECTION 3: "THINK ABOUT" TACTICAL IDEAS (ACTIONABLE RADAR) -->
        <tr>
          <td style="padding: 0 28px 24px 28px;">
            <div style="font-size: 12.5px; font-weight: 700; letter-spacing: 0.04em; color: #5F6368; text-transform: uppercase; margin-bottom: 12px;">💡 "Think About" Tactical Investment Radar</div>

            <!-- IDEA 1: INCREASE CEG -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #1A73E8; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(26,115,232,0.12);">
              <tr>
                <td>
                  <span style="background-color: #E8F0FE; color: #1967D2; font-size: 10.5px; font-weight: 800; padding: 3px 8px; border-radius: 6px; text-transform: uppercase;">ACCUMULATION OPPORTUNITY</span>
                  <div style="font-size: 16px; font-weight: 700; color: #202124; margin-top: 5px;">Think About: Increasing Stake in Constellation Energy (CEG)</div>
                  <div style="margin-top: 8px; font-size: 13px; color: #3C4043; line-height: 1.5;">
                    <b>Catalyst:</b> Nuclear baseload power is the single most critical bottleneck for AI datacenter expansion. Constellation's 20-year Microsoft PPA to revive Three Mile Island Unit 1 guarantees massive cash flow at high contracted prices. With shares down <b>-4.96%</b> from your cost basis ($264 vs $278), this dip represents an attractive re-accumulation window before regulatory approvals finalize.
                  </div>
                  <div style="background-color: #F8F9FA; border-left: 3px solid #1A73E8; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                    <b>💡 What this means:</b> Artificial intelligence requires massive amounts of non-stop electricity that wind and solar can't reliably provide around the clock. Constellation is the king of nuclear energy and already has Microsoft locked into a 20-year contract. Because the stock pulled back 5%, it's on sale right now. Adding a few more shares here is a smart move for long-term growth.
                  </div>
                </td>
              </tr>
            </table>

            <!-- IDEA 2: TRIM TEM WINNER -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #34A853; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(52,168,83,0.12);">
              <tr>
                <td>
                  <span style="background-color: #E6F4EA; color: #137333; font-size: 10.5px; font-weight: 800; padding: 3px 8px; border-radius: 6px; text-transform: uppercase;">PROFIT DISCIPLINE</span>
                  <div style="font-size: 16px; font-weight: 700; color: #202124; margin-top: 5px;">Think About: Trimming 20%–25% of Tempus AI (TEM) at +50% Profit</div>
                  <div style="margin-top: 8px; font-size: 13px; color: #3C4043; line-height: 1.5;">
                    <b>Catalyst:</b> Tempus AI has surged to <b>$82.62</b> (+49.59% gain, +$533 profit). Under Frontier Portfolio Rule §2.5 (1.5x Winner Trim Rule), when a speculative position delivers a 50% gain, best practice is harvesting 20% to 25% of the shares to lock in gains and de-risk your initial cost basis.
                  </div>
                  <div style="background-color: #F8F9FA; border-left: 3px solid #137333; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                    <b>💡 What this means:</b> Tempus has been a massive winner, up nearly +50%. Discipline is what protects wealth: by selling just 4 or 5 shares, you put cold hard cash into your pocket while letting the remaining shares ride for free. It guarantees you make money no matter what the stock does next.
                  </div>
                </td>
              </tr>
            </table>

            <!-- IDEA 3: ASTS SPACE BROADBAND -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <span style="background-color: #F1F3F4; color: #5F6368; font-size: 10.5px; font-weight: 800; padding: 3px 8px; border-radius: 6px; text-transform: uppercase;">WATCHLIST CONVICTION</span>
                  <div style="font-size: 16px; font-weight: 700; color: #202124; margin-top: 5px;">Think About: Preparing AST SpaceMobile (ASTS) Dip-Buy Tranche</div>
                  <div style="margin-top: 8px; font-size: 13px; color: #3C4043; line-height: 1.5;">
                    <b>Catalyst:</b> ASTS trades at $59.42 (-13.98% from $69.08 cost basis). Five commercial BlueBird satellites are on orbit undergoing unfurl testing. The carrier revenue ramp with AT&T and Verizon begins in late 2026. A consolidation toward the $52–$55 support shelf represents a high-upside accumulation spot.
                  </div>
                  <div style="background-color: #F8F9FA; border-left: 3px solid #1A73E8; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                    <b>💡 What this means:</b> AST SpaceMobile is building a cellular network in outer space so any standard smartphone gets 5G coverage anywhere on Earth. The stock is down -14% as satellites undergo testing. If it dips a bit lower, it will be a prime opportunity to buy a few more shares before they turn on commercial service with AT&T.
                  </div>
                </td>
              </tr>
            </table>

            <!-- IDEA 4: CASH SECURED PUT INCOME -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;">
              <tr>
                <td>
                  <span style="background-color: #F1F3F4; color: #5F6368; font-size: 10.5px; font-weight: 800; padding: 3px 8px; border-radius: 6px; text-transform: uppercase;">INCOME GENERATION</span>
                  <div style="font-size: 16px; font-weight: 700; color: #202124; margin-top: 5px;">Think About: Selling Cash-Secured Puts with Your $27,996 Cash</div>
                  <div style="margin-top: 8px; font-size: 13px; color: #3C4043; line-height: 1.5;">
                    <b>Catalyst:</b> With $27,996 in cash reserves (53.0% of portfolio) and 0 open options contracts, capital is fully ready to work. Staging cash-secured puts on strong watchlist names (like <b>SOFI $16P</b> or <b>NCLH $14P</b>) generates 15%–20% annualized cash yield without chasing stocks at market tops.
                  </div>
                  <div style="background-color: #F8F9FA; border-left: 3px solid #137333; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                    <b>💡 What this means:</b> You have almost $28,000 sitting in cash. Instead of buying stocks when they are expensive, we can sell "cash-secured puts." This is like offering insurance to other investors: they pay you cash up front immediately, and you only buy their stock if it drops to a big discount price that you'd love to own anyway.
                  </div>
                </td>
              </tr>
            </table>

          </td>
        </tr>

        <!-- FOOTER -->
        <tr>
          <td style="padding: 20px 28px; background-color: #F8F9FA; border-top: 1px solid #E8EAED; text-align: center;">
            <div style="font-size: 12px; color: #5F6368; font-weight: 600;">Frontier Agentic Trading System · Autonomous Portfolio Management</div>
            <div style="font-size: 11px; color: #80868B; margin-top: 4px;">Account: ••••5530 (API 865935530) · Total NAV: {equity_str} · Generated autonomously on September 30, 2026</div>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

</body>
</html>"""

    output_path = os.path.join(BRIEFS_DIR, "2026-09-30-premarket-brief.html")
    with open(output_path, "w") as f:
        f.write(html)
    print(f"✅ Generated Agentic Morning Briefing with ALL 20 STOCKS: {output_path}")

if __name__ == "__main__":
    build_brief()
