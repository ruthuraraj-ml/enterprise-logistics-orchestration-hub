from crewai import Task


def create_critique_task(
    agent,
    strategy
):

    return Task(
        description=f"""
        Review the following optimization strategy.

        STRATEGY:

        {strategy}

        Critically evaluate:

        1. Strategy strengths
        2. Strategy weaknesses
        3. Missing considerations
        4. Improved recommendation
        5. Approval status

        IMPORTANT:
        Return only valid JSON.
        """,

        expected_output="""
        {
            "strategy_strengths": [
                "...",
                "..."
            ],

            "strategy_weaknesses": [
                "...",
                "..."
            ],

            "missing_considerations": [
                "...",
                "..."
            ],

            "revised_recommendation": "...",

            "approval_status": "Approved | Approved with Modifications | Rejected"
        }
        """,

        agent=agent
    )