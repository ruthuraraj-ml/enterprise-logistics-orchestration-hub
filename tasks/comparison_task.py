from crewai import Task

from models.state import ProductComparison


def create_comparison_task(
    agent,
    strategy_context
):

    return Task(

        description=f"""
        Compare the following product
        optimization strategies.

        {strategy_context}

        Determine:

        1. Which product deserves investment
        priority.

        2. Which product has the highest
        logistics risk.

        3. Which product has the highest
        expected business return.

        4. Rank implementation complexity.

        Return executive-level reasoning.
        """,

        expected_output="""
        Strategic portfolio comparison.
        """,

        output_pydantic=ProductComparison,

        agent=agent
    )