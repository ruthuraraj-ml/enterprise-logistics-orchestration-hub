import json
from crewai import Task


def create_strategy_task(
    agent,
    inventory_insights,
    route_insights,
    memory_context=None  # <-- Injected historical context safely
):
    # 1. Format the memory history cleanly for the LLM prompt context
    if memory_context and len(memory_context) > 0:
        history_prompt = json.dumps(memory_context, indent=2)
    else:
        history_prompt = "No prior historical strategies exist for this product. This is Run #1."

    return Task(
        description=f"""
        Analyze the following findings.

        INVENTORY INSIGHTS:
        {inventory_insights}

        ROUTE INSIGHTS:
        {route_insights}

        ----------------------------------------------------------------------
        🧠 HISTORICAL STRATEGY MEMORY CONTEXT:
        {history_prompt}
        ----------------------------------------------------------------------

        Your responsibilities:
        1. Determine optimization priority level
        2. Define the primary optimization goal
        3. Recommend concrete actions
        4. Estimate expected business impact
        5. Assess implementation risk

        CRITICAL DIRECTIVE - PERFORM DELTA REASONING:
        You must act as an evolving system intelligence. Do not loop back or repeat identical baseline recommendations across sequential runs if operational context has shifted.
        
        If historical strategies exist:
        - DELTA EVOLUTION: Build upon successful, ongoing historical recommendations (e.g., if a previous run recommended establishing a 3PL pilot and fresh data shows delays persist, do not recommend setting up the pilot again. Instead, advance directly to localized staging thresholds, specific carrier metrics, or inventory positioning allocations).
        - REDUNDANCY CHECK: Do not instruct the business to initiate frameworks, studies, or pilots that have already been launched or recommended in past iterations.
        - CONTRAST ANALYSIS: Factor in how current operational metrics differ from previous runs and explicitly evolve your recommended actions to match this trajectory.

        Return ONLY valid JSON.
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