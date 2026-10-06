import os
import yfinance as yf
from google import genai
from google.genai import types

class SentimentAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client()

    def run(self, tickers):
        print(f"SentimentAgent: Analyzing sentiment for {len(tickers)} tickers...")
        results = {}
        for ticker in tickers:
            print(f" -> Fetching data for {ticker}")
            try:
                # yfinance data
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
                target_mean = info.get("targetMeanPrice", 0)
                recommendation = info.get("recommendationKey", "N/A")
                
                upside = 0
                if current_price and target_mean:
                    upside = ((target_mean / current_price) - 1) * 100

                # Gemini news & chatter analysis
                prompt = f"""
                You are a quantitative sentiment analyst. Search the web for the latest news, rumors, analyst upgrades/downgrades, and market chatter regarding the stock ticker {ticker}.
                The current price is ${current_price:.2f} and the consensus analyst price target is ${target_mean:.2f} (Implied upside: {upside:.1f}%). Analyst recommendation: {recommendation}.
                
                Provide a 2-3 sentence extremely concise and insightful analysis summarizing the current sentiment, any recent rumors or catalysts, and what this means for a long-term tech investor holding this stock.
                Return ONLY the text analysis. No markdown blocks.
                """
                
                response = self.client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[{'google_search': {}}],
                        temperature=0.2,
                    )
                )
                analysis = response.text.strip()
                
                results[ticker] = {
                    "current_price": current_price,
                    "target_mean": target_mean,
                    "recommendation": recommendation,
                    "upside_pct": upside,
                    "analysis": analysis
                }
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                results[ticker] = {
                    "current_price": 0, "target_mean": 0, "recommendation": "Error", "upside_pct": 0,
                    "analysis": f"Could not fetch sentiment analysis due to an error: {e}"
                }
        return results
