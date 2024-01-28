from typing import List

from pydantic import BaseModel, Field


class StockSchema(BaseModel):
    symbol: int = Field(..., description='Stock Symbol')
    avg_price: int = Field(None, ge=0, description='Average Price')
    qty: int = Field(None, ge=0, description='Number of Units held')


class NotFoundResponseSchema(BaseModel):
    code: int = Field(404, description="Status Code")
    message: str = Field("Resource not found!", description="Exception Information")


class GetParameterSchema(BaseModel):
    symbol: str = Field(..., description='Stock Symbol')


class GetResponseSchema(BaseModel):
    code: int = Field(200, description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: StockSchema


class GetMultipleResponseSchema(BaseModel):
    code: int = Field(200, description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: List[StockSchema]


class PostBodySchema(BaseModel):
    stock_symbol: str = Field(..., description="symbolName")
    price_per_unit: float = Field(gt=0, description="Price per unit")
    units: float = Field(gt=0, description="Units Owned")
