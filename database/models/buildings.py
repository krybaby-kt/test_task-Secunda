"""
Модуль модели здания.
"""
from database.base_model import SQLAlchemyModel
from sqlalchemy import Column, Integer, String, Numeric


class BuildingModel(SQLAlchemyModel):
    __tablename__ = "buildings"
    id = Column(Integer, unique=True, primary_key=True)
    address = Column(String, unique=True, nullable=False)
    latitude   = Column(Numeric(10, 8), nullable=False)
    longitude  = Column(Numeric(11, 8), nullable=False)
