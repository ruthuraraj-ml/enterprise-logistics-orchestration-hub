from crewai import Task


def create_revision_task(
    agent,
    original_strategy,
    critique
):

    return Task(
        description=f"""
        You previously created the following strategy.

        ORIGINAL STRATEGY:

        {original_strategy}


        The following critique was provided.

        CRITIQUE:

        {critique}


        Revise the strategy.

        Requirements:

        1. Preserve valid recommendations.
        2. Address identified weaknesses.
        3. Incorporate missing considerations.
        4. Improve implementation feasibility.
        5. Improve business justification.

        IMPORTANT:

        Return only valid JSON.
        """,

        expected_output="""
        {
            "product_name": "...",

            "priority_level": "...",

            "optimization_goal": "...",

            "recommended_actions": [
                "...",
                "...",
                "..."
            ],

            "expected_business_impact": "...",

            "implementation_risk": "..."
        }
        """,

        agent=agent
    )