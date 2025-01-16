from datetime import time

from pydantic import BaseModel, Field


class GetRouteSchema(BaseModel):
    id: int
    name: str
    start_point_name: str
    end_point_name: str
    start_time: time
    end_time: time
    interval_seconds: int
    duration_seconds: int
    length_km: int = Field(..., alias="length")


class AddRouteSchema(BaseModel):
    name: str
    start_point_name: str
    end_point_name: str
    start_time: time
    end_time: time
    interval_seconds: int
    duration_seconds: int
    length_km: int


class TotalRoutesLengthSchema(BaseModel):
    total_length: int = 0
