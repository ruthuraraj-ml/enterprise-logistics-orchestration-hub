from typing import List, Dict, Any
from pydantic import BaseModel, Field


class InventoryMetrics(BaseModel):
    product_name: str

    total_units_sold: int

    total_sales: float

    average_profit: float

    sales_velocity: float

    category: str


class DeliveryMetrics(BaseModel):

    product_name: str

    avg_actual_days: float

    avg_scheduled_days: float

    avg_delay_days: float

    delay_rate: float

    high_risk_shipments: int

    shipment_count: int


class GeoMetrics(BaseModel):

    product_name: str

    top_delay_region: str

    top_delay_country: str

    top_delay_route_count: int

    delayed_shipments: int

    avg_route_distance_km: float

    high_risk_percentage: float


class LogisticsState(BaseModel):

    products: List[str] = Field(default_factory=list)
    
    optimization_type: str = Field(default="")

    inventory_metrics: Dict[str, Any] = Field(default_factory=dict)

    delivery_metrics: Dict[str, Any] = Field(default_factory=dict)

    geo_metrics: Dict[str, Any] = Field(default_factory=dict)

    inventory_insights: dict = Field(default_factory=dict)

    delivery_insights: dict = Field(default_factory=dict)

    geo_insights: dict = Field(default_factory=dict)

    strategy: Dict[str, Any] = Field(default_factory=dict)

    critique: Dict[str, Any] = Field(default_factory=dict)

    memory_context: List[Dict[str, Any]] = Field(default_factory=list)

    final_strategy: Dict[str, Any] = Field(default_factory=dict)

    reflection_required: bool = False

    revision_count: int = 0

    approval_status: str = "Pending"


class InventoryInsight(BaseModel):
    product_name: str

    inventory_classification: str

    inventory_risk: str

    key_observation: str

    recommendation: str


class RouteInsight(BaseModel):
    product_name: str

    delivery_classification: str

    logistics_risk: str

    key_observation: str

    recommendation: str


class OptimizationStrategy(BaseModel):
    product_name: str

    priority_level: str

    optimization_goal: str

    recommended_actions: list[str]

    expected_business_impact: str

    implementation_risk: str


class StrategyCritique(BaseModel):

    strategy_strengths: list[str]

    strategy_weaknesses: list[str]

    missing_considerations: list[str]

    revised_recommendation: str

    approval_status: str


class ProductComparison(BaseModel):

    recommended_investment_target: str

    highest_logistics_risk: str

    highest_expected_roi: str

    operational_complexity_ranking: List[str]

    executive_summary: str