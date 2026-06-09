from pathlib import Path
from typing import List, Optional
from math import radians, sin, cos, sqrt, atan2

import pandas as pd

from models.state import GeoMetrics


class GeoAnalyticsTool:
    """
    Analyzes geospatial delivery performance for selected products, 
    identifying true correlated geographical delay bottlenecks.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        self.df = pd.read_csv(self.dataset_path)

    @staticmethod
    def _haversine_distance(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate great-circle distance between two points
        on Earth using the Haversine formula.
        Returns distance in kilometers.
        """
        R = 6371.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            sin(dlat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def _calculate_metrics(
        self,
        product_df: pd.DataFrame,
        product_name: str
    ) -> GeoMetrics:

        # Calculate route distances using origin and destination geolocations
        distances = product_df.apply(
            lambda row: self._haversine_distance(
                row["latitude_src"],
                row["longitude_src"],
                row["latitude_dest"],
                row["longitude_dest"]
            ),
            axis=1
        )

        avg_route_distance_km = round(distances.mean(), 2)

        # Filter specifically for late shipments to extract geospatial bottlenecks
        delayed_df = product_df[product_df["late_delivery_risk"] == 1]
        delayed_shipments = len(delayed_df)

        high_risk_percentage = round(
            product_df["late_delivery_risk"].mean() * 100,
            2
        )

        if delayed_df.empty:
            top_delay_region = "N/A"
            top_delay_country = "N/A"
            top_delay_route_count = 0
        else:
            # FIX: Group fields together to avoid pairing mismatched regions and countries
            route_counts = (
                delayed_df.groupby(["order_region", "order_country"])
                .size()
            )
            
            top_route = route_counts.idxmax()
            top_delay_route_count = int(route_counts.max())
            
            top_delay_region = top_route[0]
            top_delay_country = top_route[1]

        return GeoMetrics(
            product_name=product_name,
            top_delay_region=top_delay_region,
            top_delay_country=top_delay_country,
            top_delay_route_count=top_delay_route_count,
            delayed_shipments=delayed_shipments,
            avg_route_distance_km=avg_route_distance_km,
            high_risk_percentage=high_risk_percentage
        )

    def run(
        self,
        products: List[str],
        top_n: Optional[int] = None
    ) -> List[GeoMetrics]:

        results = []

        # Product-specific analysis branch
        if products:
            for product in products:
                product_df = self.df[self.df["product_name"] == product]

                if product_df.empty:
                    print(f"Warning: Product not found -> {product}")
                    continue

                metrics = self._calculate_metrics(product_df, product)
                results.append(metrics)

            return results

        # Top-N highest risk products branch
        if top_n:
            grouped = self.df.groupby("product_name")
            temp_results = []

            for product_name, product_df in grouped:
                shipment_count = len(product_df)

                # Filter low-volume statistical noise (Threshold >= 20 orders)
                if shipment_count < 20:
                    continue

                metrics = self._calculate_metrics(product_df, product_name)
                temp_results.append(metrics)

            # Sort products by total risk percentage descending
            temp_results.sort(
                key=lambda x: x.high_risk_percentage,
                reverse=True
            )

            return temp_results[:top_n]

        return results