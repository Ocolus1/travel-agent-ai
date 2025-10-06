from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from typing import List
from ai_travel_agent.tools.custom_tool import CalendarGeneratorTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AiTravelAgent():
    """AiTravelAgent crew for generating personalized travel itineraries"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # Initialize tools
    def __init__(self):
        super().__init__()
        try:
            self.search_tool = SerperDevTool()
        except Exception as e:
            print(f"Warning: SerperDevTool initialization failed: {e}")
            self.search_tool = None
        self.calendar_tool = CalendarGeneratorTool()
    
    # Travel-specific agents
    @agent
    def destination_researcher(self) -> Agent:
        """Agent responsible for researching travel destinations"""
        tools = [self.search_tool] if self.search_tool else []
        return Agent(
            config=self.agents_config['destination_researcher'], # type: ignore[index]
            tools=tools,
            verbose=True
        )

    @agent
    def itinerary_planner(self) -> Agent:
        """Agent responsible for creating detailed day-by-day itineraries"""
        return Agent(
            config=self.agents_config['itinerary_planner'], # type: ignore[index]
            verbose=True
        )

    @agent
    def calendar_formatter(self) -> Agent:
        """Agent responsible for formatting itineraries for calendar export"""
        return Agent(
            config=self.agents_config['calendar_formatter'], # type: ignore[index]
            tools=[self.calendar_tool],
            verbose=True
        )

    # Travel-specific tasks
    @task
    def research_destination_task(self) -> Task:
        """Task for researching travel destinations"""
        return Task(
            config=self.tasks_config['research_destination_task'], # type: ignore[index]
        )

    @task
    def plan_itinerary_task(self) -> Task:
        """Task for planning the detailed itinerary"""
        import os
        os.makedirs('exports', exist_ok=True)
        return Task(
            config=self.tasks_config['plan_itinerary_task'], # type: ignore[index]
            output_file='exports/travel_itinerary.md'
        )

    @task
    def format_calendar_task(self) -> Task:
        """Task for formatting itinerary as calendar events"""
        import os
        os.makedirs('exports', exist_ok=True)
        return Task(
            config=self.tasks_config['format_calendar_task'], # type: ignore[index]
            output_file='exports/calendar_events.txt'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiTravelAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=False,  # Disable memory to avoid timeout prompts
            embedder=None,  # Disable embedder
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
