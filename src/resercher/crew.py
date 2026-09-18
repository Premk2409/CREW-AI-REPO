import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Load environment variables
load_dotenv()

@CrewBase
class AIResearchCrew:
    """AI Research Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/task.yaml"

    @property
    def llm(self) -> LLM:
        api_key = os.getenv("OPENROUTER_API_KEY")
        model_name = os.getenv("OPENROUTER_MODEL", "openrouter/google/gemini-2.5-flash")
        return LLM(
            model=model_name,
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            temperature=0.7,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def research_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["research_reviewer"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["analysis_task"],
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by @agent
            tasks=self.tasks,    # Automatically collected by @task
            process=Process.sequential,
            verbose=True,
        )
