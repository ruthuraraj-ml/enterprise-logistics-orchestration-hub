from pathlib import Path
from typing import List, Optional

import pandas as pd

from models.state import InventoryMetrics


class InventoryAnalyticsTool:
    """
    Analyzes inventory-related metrics for selected products.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        self.df = pd.read_csv(self.dataset_path)

        # Convert date column once during initialization
        self.df["order_date_dateorders"] = pd.to_datetime(
            self.df["order_date_dateorders"],
            format="%d-%m-%Y %H:%M",
            errors="coerce"
        )

    def _calculate_metrics(
        self,
        product_df: pd.DataFrame,
        product_name: str
    ) -> InventoryMetrics:

        total_units_sold = int(
            product_df["order_item_quantity"].sum()
        )

        total_sales = float(
            product_df["sales"].sum()
        )

        average_profit = float(
            product_df["order_profit_per_order"].mean()
        )

        category = str(
            product_df["category_name"].iloc[0]
        )

        min_date = product_df["order_date_dateorders"].min()
        max_date = product_df["order_date_dateorders"].max()

        active_days = max(
            (max_date - min_date).days + 1,
            1
        )

        sales_velocity = round(
            total_units_sold / active_days,
            2
        )

        return InventoryMetrics(
            product_name=product_name,
            total_units_sold=total_units_sold,
            total_sales=round(total_sales, 2),
            average_profit=round(average_profit, 2),
            sales_velocity=sales_velocity,
            category=category
        )

    def run(
        self,
        products: List[str],
        top_n: Optional[int] = None
    ) -> List[InventoryMetrics]:

        results = []

        # Case 1: Specific products supplied
        if products:

            for product in products:

                product_df = self.df[
                    self.df["product_name"] == product
                ]

                if product_df.empty:
                    print(
                        f"Warning: Product not found -> {product}"
                    )
                    continue

                metrics = self._calculate_metrics(
                    product_df,
                    product
                )

                results.append(metrics)

            return results

        # Case 2: Return Top-N by sales velocity
        if top_n:

            grouped = self.df.groupby("product_name")

            temp_results = []

            for product_name, product_df in grouped:

                metrics = self._calculate_metrics(
                    product_df,
                    product_name
                )

                temp_results.append(metrics)

            temp_results.sort(
                key=lambda x: x.sales_velocity,
                reverse=True
            )

            return temp_results[:top_n]

        return results