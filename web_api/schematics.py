"""
Модуль для схем FastAPI.
"""
from pydantic import BaseModel
from typing import List


class Activity(BaseModel):
    """
    Модель деятельности.
    """
    id: int
    name: str


class PhoneNumber(BaseModel):
    """
    Модель телефонного номера.
    """
    id: int
    phone_number: str


class BuildingInfo(BaseModel):
    """
    Модель здания.
    """
    id: int
    address: str
    latitude: float
    longitude: float


class OrganizationInfo(BaseModel):
    """
    Модель организации.
    """
    id: int
    name: str
    phone_numbers: List[PhoneNumber]
    building: BuildingInfo
    activities: List[Activity]
