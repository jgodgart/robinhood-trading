import os
from google import genai
from google.genai import types
from agents.config import GEMINI_MODEL

class MacroAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY not set. MacroAgent may fail.")
        self.client = genai.Client()

    def run(self):
        print("MacroAgent: Gathering macroeconomic data...")
        prompt = """
        You are a top-tier macroeconomic analyst. Your task is to provide a comprehensive morning briefing on the current state of the global macroeconomy.
        Please search the web for the latest financial news, Federal Reserve calendar updates, interest rate expectations, and significant political headlines affecting the stock market today.
        
        Provide a concise summary focused on:
        1. Broad Market Health (S&P 500, VIX, Yields)
        2. Federal Reserve & Interest Rates
        3. Political/Geopolitical Moves affecting the market
        4. Direct implications for Tech and Frontier Equity markets (Semiconductors, Quantum, AI, Space).
        
        Then, crucially, you MUST go through EACH of the 11 core market sectors, provide information about what's happening in that sector today, and list the top stocks to consider for investment based on the current news. The 11 sectors are:
        - Information Technology: software, hardware, semiconductors, IT services (e.g., Apple, Microsoft, Nvidia).
        - Financials: banks, insurance firms, asset managers, credit cards (e.g., Berkshire Hathaway, JPMorgan Chase).
        - Healthcare: drug makers, biotech, medical devices, health insurers (e.g., Eli Lilly, UnitedHealth, Johnson & Johnson).
        - Consumer Discretionary: non-essential goods, cars, luxury items, entertainment (e.g., Amazon, Tesla, McDonald's).
        - Communication Services: telecom, media, search engines, social platforms (e.g., Alphabet, Meta Platforms).
        - Industrials: aerospace, defense, machinery, transportation, construction (e.g., Caterpillar, UPS, RTX).
        - Consumer Staples: essential everyday goods, food, beverages (e.g., Procter & Gamble, Walmart, Costco).
        - Energy: oil, natural gas, refining, renewable energy production (e.g., ExxonMobil, Chevron).
        - Materials: chemicals, mining, forestry, metal production (e.g., Linde, Sherwin-Williams).
        - Real Estate: REITs, property management/development (e.g., American Tower, Simon Property Group).
        - Utilities: electric, gas, water, renewable power infrastructure (e.g., NextEra Energy, Duke Energy).
        
        Keep it professional, analytical, and highly actionable. Format the 11 sectors in a clean, readable layout (e.g. using basic <div>, <b>, <ul>, and <h3> tags). Return the ENTIRE result as an HTML snippet suitable for embedding directly inside an email body. Do NOT wrap the response in ```html markdown blocks.
"""
        
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.2,
                )
            )
            # Strip markdown wrapper if present
            text = response.text.strip()
            if text.startswith("```html"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()
        except Exception as e:
            print(f"MacroAgent failed to generate content: {e}")
            return "<div><p><i>Macroeconomic analysis temporarily unavailable.</i></p></div>"
