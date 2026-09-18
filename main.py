import os
import sys
from dotenv import load_dotenv
from crewai.project.crew_loader import load_crew

# Load environment variables
load_dotenv()

def main():
    print("=" * 60)
    print("Loading Indian Stock Market Analyst Crew from crew.jsonc...")
    print("=" * 60)
    
    # Ensure the root tools folder is in sys.path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    crew_path = os.path.join(project_dir, "crew.jsonc")
    try:
        crew, default_inputs = load_crew(crew_path)
    except Exception as e:
        print(f"[Error] Failed to load crew configuration: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Run analysis on a major Indian equity: RELIANCE
    stock_symbol = "RELIANCE"
    print(f"\nRunning analysis for stock: {stock_symbol}...")
    print("Starting multi-agent execution (Financial Analyst ➔ Technical Analyst)...")
    print("-" * 60)
    
    try:
        result = crew.kickoff(inputs={"stock_symbol": stock_symbol})
        print("\n" + "=" * 60)
        print("Crew execution finished successfully!")
        print("=" * 60)
        print("\n### EXECUTION REPORT:\n")
        print(result)
    except Exception as e:
        print(f"[Error] Execution failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
