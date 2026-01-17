"""
Advanced Statistics Schemas

Schemas for detailed analytics and reporting.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional
from datetime import date


class StatusBreakdown(BaseModel):
    """Status breakdown with counts."""
    status: str
    count: int
    percentage: float


class ConversionMetrics(BaseModel):
    """Conversion rate metrics."""
    applied_to_screening: Optional[float] = Field(None, description="% of applied that moved to screening")
    screening_to_interview: Optional[float] = Field(None, description="% of screening that moved to interview")
    interview_to_offer: Optional[float] = Field(None, description="% of interviewed that got offer")
    offer_to_hired: Optional[float] = Field(None, description="% of offers that were accepted")
    overall_conversion: Optional[float] = Field(None, description="% of applied that were hired")


class StageTimeMetrics(BaseModel):
    """Average time spent in each stage."""
    stage: str
    avg_days: float
    min_days: float
    max_days: float
    count: int


class FunnelStage(BaseModel):
    """Funnel visualization stage data."""
    stage: str
    count: int
    percentage: float
    color: str


class DailyTrend(BaseModel):
    """Daily application trend data."""
    date: str
    count: int


class AdvancedStatsResponse(BaseModel):
    """
    Advanced statistics response for Chart.js visualization.
    
    Ready for frontend charting libraries.
    """
    # Summary
    total_applications: int = Field(..., description="Total number of applications")
    date_range: Dict[str, Optional[str]] = Field(..., description="Date range for stats")
    
    # Status breakdown
    status_breakdown: List[StatusBreakdown] = Field(..., description="Applications by status")
    
    # Conversion metrics
    conversion_metrics: ConversionMetrics = Field(..., description="Conversion rates through funnel")
    
    # Time metrics
    avg_time_per_stage: List[StageTimeMetrics] = Field(..., description="Time spent in each stage")
    
    # Funnel data (Chart.js ready)
    funnel_data: Dict[str, List] = Field(
        ...,
        description="Funnel chart data with labels and values"
    )
    
    # Daily trends (Chart.js ready)
    daily_trends: Dict[str, List] = Field(
        ...,
        description="Daily application trends with dates and counts"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_applications": 150,
                "date_range": {
                    "from": "2026-01-01",
                    "to": "2026-01-31"
                },
                "status_breakdown": [
                    {"status": "SUBMITTED", "count": 50, "percentage": 33.33},
                    {"status": "SCREENING", "count": 40, "percentage": 26.67}
                ],
                "conversion_metrics": {
                    "applied_to_screening": 80.0,
                    "screening_to_interview": 75.0,
                    "interview_to_offer": 60.0,
                    "offer_to_hired": 85.0,
                    "overall_conversion": 30.6
                },
                "avg_time_per_stage": [
                    {
                        "stage": "SUBMITTED",
                        "avg_days": 2.5,
                        "min_days": 1.0,
                        "max_days": 5.0,
                        "count": 50
                    }
                ],
                "funnel_data": {
                    "labels": ["Applied", "Screening", "Interview", "Offer", "Hired"],
                    "values": [100, 80, 60, 40, 30],
                    "colors": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
                },
                "daily_trends": {
                    "labels": ["2026-01-01", "2026-01-02"],
                    "values": [5, 8]
                }
            }
        }
    )
