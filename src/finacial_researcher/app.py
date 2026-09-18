import os
import sys
import gradio as gr
from dotenv import load_dotenv

# Ensure the project directory is in sys.path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from crewai.project.crew_loader import load_crew

# Load environment variables
load_dotenv()

def run_financial_research(stock_symbol):
    if not stock_symbol or not stock_symbol.strip():
        return "Please enter a valid stock symbol."

    ticker = stock_symbol.strip().upper()
    
    # Load the JSON-first crew
    crew_path = os.path.join(project_dir, "crew.jsonc")
    try:
        crew, default_inputs = load_crew(crew_path)
    except Exception as e:
        return f"Error loading crew configuration: {str(e)}"

    # Run the crew with the provided stock symbol
    try:
        result = crew.kickoff(inputs={"stock_symbol": ticker})
        return str(result)
    except Exception as e:
        return f"Error executing stock analysis crew: {str(e)}"


# Define Gradio UI
with gr.Blocks(title="Indian Market Stock Analyst") as app:
    gr.Markdown(
        """
        # 📈 Indian Market Stock Analyst
        
        ### 👨‍💼 Fundamental Analyst ➔ 📊 Technical Analyst
        
        Enter any Indian Stock ticker (NSE/BSE) to perform a comprehensive fundamental financial evaluation and a technical price-action analysis. It will provide:
        - **Long-term investment options** (intrinsic value, ROE, debt health, growth metrics)
        - **Short-term swing/trading options** (trend, 50/200 MA, support/resistance, entry, targets, and stop-loss)
        """
    )
    
    with gr.Row():
        stock_input = gr.Textbox(
            label="Stock Symbol / Ticker (NSE/BSE)",
            placeholder="e.g. RELIANCE, TCS, INFY, SBIN, COALINDIA",
            value="RELIANCE"
        )
    
    run_button = gr.Button("🔍 Run Analysis", variant="primary")
    
    report_output = gr.Markdown(label="Stock Analysis Report")
    
    run_button.click(
        fn=run_financial_research,
        inputs=[stock_input],
        outputs=report_output
    )

if __name__ == "__main__":
    app.launch(share=True)
