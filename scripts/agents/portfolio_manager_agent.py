import os
import json
from google import genai
from google.genai import types

class PortfolioManagerAgent:
    def __init__(self, state_file, agents_md_file):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client()
        self.state_file = state_file
        self.agents_md_file = agents_md_file

    def run(self, sentiment_data):
        print("PortfolioManagerAgent: Generating Think About tactical recommendations...")
        
        # Load state
        with open(self.state_file, "r") as f:
            state = json.load(f)
            
        # Load rules
        with open(self.agents_md_file, "r") as f:
            rules = f.read()
            
        # Prepare context for the prompt
        agentic_state = state.get("agentic", {})
        
        prompt = f"""
        You are the Portfolio Guardian for the Frontier Agentic Trading System.
        Read the following rules from AGENTS.md carefully:
        {rules}
        
        Here is the current live state of the Agentic portfolio:
        Total Equity: {agentic_state.get('equity_nav')}
        Cash: {agentic_state.get('equity_nav', 0) - agentic_state.get('market_value', 0)}
        
        Here is the sentiment and analyst data for our holdings:
        {json.dumps(sentiment_data, indent=2)}
        
        Based on the strict rules (e.g. 1.5x Winner Trim Rule, drawdown accumulation) and the sentiment data, generate 3-4 concrete, highly actionable 'Think About' tactical recommendations.
        Format each recommendation exactly like this in HTML:
        
        <!-- IDEA X -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFFF; border: 1px solid #1A73E8; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(26,115,232,0.12);">
            <tr>
            <td>
                <span style="background-color: #E8F0FE; color: #1967D2; font-size: 10.5px; font-weight: 800; padding: 3px 8px; border-radius: 6px; text-transform: uppercase;">[CATEGORY]</span>
                <div style="font-size: 16px; font-weight: 700; color: #202124; margin-top: 5px;">Think About: [Actionable Title]</div>
                <div style="margin-top: 8px; font-size: 13px; color: #3C4043; line-height: 1.5;">
                <b>Catalyst:</b> [Why are we doing this based on data/sentiment/rules]
                </div>
                <div style="background-color: #F8F9FA; border-left: 3px solid #1A73E8; border-radius: 4px; padding: 8px 12px; margin-top: 10px; font-size: 12px; color: #3C4043; line-height: 1.45;">
                <b>💡 What this means:</b> [Clear, simple explanation without using cliches.]
                </div>
            </td>
            </tr>
        </table>
        
        Provide only the HTML output. Do not wrap in ```html markdown. Ensure we never suggest buying stocks from the Self-Managed account for the Agentic account.
        """
        
        response = self.client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
            )
        )
        
        text = response.text.strip()
        if text.startswith("```html"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
