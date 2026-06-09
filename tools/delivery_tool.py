from pathlib import Path
from typing import List, Optional

import pandas as pd

from models.state import DeliveryMetrics


class DeliveryAnalyticsTool:
    """
    Analyzes delivery performance metrics for selected products.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        self.df = pd.read_csv(self.dataset_path)

    def _calculate_metrics(
        self,
        product_df: pd.DataFrame,
        product_name: str
    ) -> DeliveryMetrics:
        
        avg_actual_days = round(
            product_df["days_for_shipping_real"].mean(),
            2
        )

        avg_scheduled_days = round(
            product_df["days_for_shipment_scheduled"].mean(),
            2
        )

        avg_delay_days = round(
            avg_actual_days - avg_scheduled_days,
            2
        )

        high_risk_shipments = int(
            product_df["late_delivery_risk"].sum()
        )

        delay_rate = round(
            product_df["late_delivery_risk"].mean() * 100,
            2
        )

        return DeliveryMetrics(
            product_name=product_name,
            avg_actual_days=avg_actual_days,
            avg_scheduled_days=avg_scheduled_days,
            avg_delay_days=avg_delay_days,
            delay_rate=delay_rate,
            high_risk_shipments=high_risk_shipments,
            shipment_count = len(product_df)
        )

    def run(
        self,
        products: List[str],
        top_n: Optional[int] = None
    ) -> List[DeliveryMetrics]:
        
        results = []

        # Specific products
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

        # Top-N by delay rate
        if top_n:

            grouped = self.df.groupby("product_name")

            temp_results = []

            for product_name, product_df in grouped:

                shipment_count = len(product_df)

                if shipment_count < 20:
                    continue

                metrics = self._calculate_metrics(
                    product_df,
                    product_name
                )

                temp_results.append(metrics)

            temp_results.sort(
                key=lambda x: x.delay_rate,
                reverse=True
            )

            return temp_results[:top_n]

        return results