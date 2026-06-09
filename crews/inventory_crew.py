from crewai import Crew

from agents.inventory_analyst import (
    create_inventory_analyst
)

from tasks.inventory_analysis_task import (
    create_inventory_analysis_task
)


def run_inventory_crew(
    inventory_metrics
):

    analyst = create_inventory_analyst()

    task = create_inventory_analysis_task(
        analyst,
        inventory_metrics
    )

    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()