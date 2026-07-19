from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from aikubagent.config.llm import llm


@CrewBase
class Aikubagent():
    """Aikubagent crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def incident_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["incident_analyst"],
            llm=llm,
            verbose=True,
        )

    @task
    def analyze_incident(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_incident"],
            agent=self.incident_analyst(),   # <-- Add this
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Aikubagent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
