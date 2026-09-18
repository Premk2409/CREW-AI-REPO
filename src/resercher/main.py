from crew import AIResearchCrew

if __name__ == "__main__":

    inputs = {
        "topic": "Generative AI and AI Agents",
        "month": "September",
        "year": "2026"
    }

    result = AIResearchCrew().crew().kickoff(
        inputs=inputs
    )

    print("\n===== FINAL RESEARCH REPORT =====\n")
    print(result)