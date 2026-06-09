from memory.strategy_store import (
    StrategyMemory
)

from crews.comparison_crew import (
    run_comparison_crew
)

memory = StrategyMemory()

products = [
    "Smart watch",
    "Nike Men's CJ Elite 2 TD Football Cleat"
]

strategies = {}

for product in products:

    strategy = (
        memory.get_latest_strategy(product)
    )

    if strategy:
        strategies[product] = strategy

result = run_comparison_crew(
    strategies
)

print(result)