from crewai import Crew

from agents.critic import (
    create_critic
)

from tasks.critique_task import (
    create_critique_task
)


def run_critique_crew(
    strategy
):

    critic = create_critic()

    task = create_critique_task(
        critic,
        strategy
    )

    crew = Crew(
        agents=[critic],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()