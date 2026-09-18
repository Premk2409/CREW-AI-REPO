import os
import yfinance as yf
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class StockFetcherInput(BaseModel):
    """Input schema for StockFetcherTool."""
    symbol: str = Field(..., description="Stock symbol of the Indian market, e.g. RELIANCE, TCS, INFY")

class StockFetcherTool(BaseTool):
    name: str = "stock_fetcher"
    description: str = "Fetches comprehensive real-time financial, fundamental, and technical price data for a given Indian stock symbol."
    args_schema: Type[BaseModel] = StockFetcherInput

    def _run(self, symbol: str) -> str:
        # Append NSE suffix if not present
        ticker_symbol = symbol.strip().upper()
        if not (ticker_symbol.endswith(".NS") or ticker_symbol.endswith(".BO")):
            ticker_symbol = f"{ticker_symbol}.NS"
        
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            # Extract key financials safely
            company_name = info.get("longName", ticker_symbol)
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            current_price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
            
            market_cap = info.get("marketCap", "N/A")
            if isinstance(market_cap, (int, float)):
                market_cap_str = f"₹{market_cap:,}"
            else:
                market_cap_str = str(market_cap)
                
            pe_ratio = info.get("trailingPE", "N/A")
            forward_pe = info.get("forwardPE", "N/A")
            pb_ratio = info.get("priceToBook", "N/A")
            
            dividend_yield = info.get("dividendYield", "N/A")
            dividend_yield_str = f"{dividend_yield * 100:.2f}%" if isinstance(dividend_yield, float) else "N/A"
            
            ebitda = info.get("ebitda", "N/A")
            if isinstance(ebitda, (int, float)):
                ebitda_str = f"₹{ebitda:,}"
            else:
                ebitda_str = str(ebitda)
                
            debt_to_equity = info.get("debtToEquity", "N/A")
            
            return_on_equity = info.get("returnOnEquity", "N/A")
            roe_str = f"{return_on_equity * 100:.2f}%" if isinstance(return_on_equity, float) else "N/A"
            
            free_cash_flow = info.get("freeCashflow", "N/A")
            if isinstance(free_cash_flow, (int, float)):
                fcf_str = f"₹{free_cash_flow:,}"
            else:
                fcf_str = str(free_cash_flow)
                
            revenue_growth = info.get("revenueGrowth", "N/A")
            rev_growth_str = f"{revenue_growth * 100:.2f}%" if isinstance(revenue_growth, float) else "N/A"
            
            earnings_growth = info.get("earningsGrowth", "N/A")
            earn_growth_str = f"{earnings_growth * 100:.2f}%" if isinstance(earnings_growth, float) else "N/A"
            
            fifty_two_week_high = info.get("fiftyTwoWeekHigh", "N/A")
            fifty_two_week_low = info.get("fiftyTwoWeekLow", "N/A")
            fifty_day_ma = info.get("fiftyDayAverage", "N/A")
            two_hundred_day_ma = info.get("twoHundredDayAverage", "N/A")
            volume = info.get("volume", "N/A")
            average_volume = info.get("averageVolume", "N/A")
            
            # Fetch recent price history for momentum analysis
            history = ticker.history(period="1mo")
            recent_prices = []
            if not history.empty:
                for date, row in history.iterrows():
                    recent_prices.append(f"{date.strftime('%Y-%m-%d')}: Close=₹{row['Close']:.2f}, Vol={row['Volume']:.0f}")
                recent_prices_str = "\n".join(recent_prices[-10:]) # last 10 trading days
            else:
                recent_prices_str = "No recent history available"
            
            output = (
                f"=== Stock Report for {company_name} ({ticker_symbol}) ===\n"
                f"Sector: {sector} | Industry: {industry}\n\n"
                f"--- Market & Valuation Metrics ---\n"
                f"Current Price: ₹{current_price}\n"
                f"Market Cap: {market_cap_str}\n"
                f"Trailing P/E: {pe_ratio} | Forward P/E: {forward_pe}\n"
                f"Price to Book (P/B): {pb_ratio}\n"
                f"Dividend Yield: {dividend_yield_str}\n\n"
                f"--- Financial Health & Growth ---\n"
                f"EBITDA: {ebitda_str}\n"
                f"Debt to Equity Ratio: {debt_to_equity}\n"
                f"Return on Equity (ROE): {roe_str}\n"
                f"Free Cash Flow: {fcf_str}\n"
                f"Quarterly Revenue Growth (YoY): {rev_growth_str}\n"
                f"Quarterly Earnings Growth (YoY): {earn_growth_str}\n\n"
                f"--- Technical Indicators ---\n"
                f"52-Week Range: ₹{fifty_two_week_low} - ₹{fifty_two_week_high}\n"
                f"50-Day Moving Average: ₹{fifty_day_ma}\n"
                f"200-Day Moving Average: ₹{two_hundred_day_ma}\n"
                f"Current Volume: {volume} | 10-Day Avg Volume: {average_volume}\n\n"
                f"--- Recent Price Action (Last 10 Days) ---\n"
                f"{recent_prices_str}\n"
            )
            return output
        except Exception as e:
            return f"Error fetching stock data for {ticker_symbol}: {str(e)}"
