from crewai import Crew

from agents.strategist import (
    create_strategist
)

from tasks.revision_task import (
    create_revision_task
)


def run_revision_crew(
    strategy,
    critique
):

    strategist = create_strategist()

    task = create_revision_task(
        strategist,
        strategy,
        critique
    )

    crew = Crew(
        agents=[strategist],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()