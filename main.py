import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM

# Load environment variables from .env
load_dotenv()

def main():
    # 1. Retrieve & validate environment configurations
    api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("OPENROUTER_MODEL", "openrouter/google/gemini-2.5-flash")

    if not api_key or api_key == "your_openrouter_api_key_here":
        print("[Error] Please set your 'OPENROUTER_API_KEY' in the .env file.", file=sys.stderr)
        print("Get your key at: https://openrouter.ai/keys", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing CrewAI with OpenRouter LLM...")
    print(f"Target Model: {model_name}")
    print("=" * 60)

    # 2. Configure the LLM for OpenRouter integration
    # CrewAI utilizes LiteLLM under the hood. Setting base_url and passing the
    # 'openrouter/' prefix ensures clean and correct routing.
    openrouter_llm = LLM(
        model=model_name,
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.7,
    )

    # 3. Define the Agents
    # Each agent represents a specialized persona with unique skills and goals.
    research_agent = Agent(
        role="Senior Technology Researcher",
        goal="Uncover groundbreaking advancements, key players, and future directions in {topic}",
        backstory=(
            "You are an elite research analyst at a top-tier advisory firm. "
            "You possess an exceptional ability to separate hype from true "
            "innovation and provide deep, data-driven synthesis."
        ),
        llm=openrouter_llm,
        verbose=True,
    )

    writer_agent = Agent(
        role="Lead Technical Writer",
        goal="Synthesize complex technical research into an engaging, structured, and easy-to-read executive brief on {topic}",
        backstory=(
            "You are a seasoned technology journalist and copywriter. "
            "Your superpower is translating dense technical insights into elegant, "
            "persuasive prose that captivates both executives and developers alike."
        ),
        llm=openrouter_llm,
        verbose=True,
    )

    # 4. Define the Tasks
    # Tasks define the operational flow and tie directly to specific agents.
    research_task = Task(
        description=(
            "Conduct an in-depth research on the latest developments in {topic}. "
            "Identify major advancements, key technical breakthroughs, and critical challenges."
        ),
        expected_output="A detailed bulleted summary of findings, key trends, and technology roadblocks.",
        agent=research_agent,
    )

    writing_task = Task(
        description=(
            "Review the research findings and write an executive briefing. "
            "The brief should have an engaging title, a clear introduction, "
            "sections for key advancements, and a forward-looking conclusion."
        ),
        expected_output="A beautifully styled Markdown executive brief ready for publication.",
        agent=writer_agent,
    )

    # 5. Assemble the Crew
    # We orchestrate our agents sequentially.
    crew = Crew(
        agents=[research_agent, writer_agent],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )

    # 6. Kickoff the execution
    # Provide input variables to the {topic} placeholders
    inputs = {
        "topic": "AI Agent Orchestration & CrewAI Multi-Agent Frameworks"
    }
    
    print("\nStarting Crew execution...")
    result = crew.kickoff(inputs=inputs)

    print("\n" + "=" * 60)
    print("Crew execution finished successfully!")
    print("=" * 60)
    print("\n### Execution Output:\n")
    print(result)

if __name__ == "__main__":
    main()
