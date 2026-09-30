import os
from google import genai
from google.genai import types

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
        
        Keep it professional, analytical, and highly actionable. Return the result in HTML format suitable for embedding inside an email body (e.g. using basic <div>, <b>, <ul> tags). Do NOT wrap the response in ```html markdown blocks.
        """
        
        response = self.client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{'google_search': {}}],
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
