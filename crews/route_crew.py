from crewai import Crew

from agents.route_analyst import (
    create_route_analyst
)

from tasks.route_analysis_task import (
    create_route_analysis_task
)


def run_route_crew(
    delivery_metrics,
    geo_metrics
):

    analyst = create_route_analyst()

    task = create_route_analysis_task(
        analyst,
        delivery_metrics,
        geo_metrics
    )

    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()