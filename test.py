from services.product_catalog import ProductCatalog
from memory.strategy_store import StrategyMemory


catalog = ProductCatalog()

memory = StrategyMemory()

print("\nDATASET PRODUCTS")
print(len(catalog.get_all_products()))

print("\nMEMORY PRODUCTS")
print(memory.get_all_products())

print("\nLATEST STRATEGY")
print(
    memory.get_latest_strategy(
        "Smart watch"
    )
)

print("\nTIMELINE")
print(
    memory.get_product_run_timeline(
        "Smart watch"
    )
)