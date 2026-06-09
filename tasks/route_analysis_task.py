from crewai import Task


def create_route_analysis_task(
    agent,
    delivery_metrics,
    geo_metrics
):

    return Task(
        description=f"""
        Analyze the following delivery metrics:

        DELIVERY METRICS:
        {delivery_metrics}

        GEO METRICS:
        {geo_metrics}

        Determine:

        1. Delivery classification
        2. Logistics risk level
        3. Key observation
        4. Operational recommendation

        Return output as JSON.
        """,

        expected_output="""
        {{
            "product_name": "...",
            "delivery_classification": "...",
            "logistics_risk": "...",
            "key_observation": "...",
            "recommendation": "..."
        }}
        """,

        agent=agent
    )