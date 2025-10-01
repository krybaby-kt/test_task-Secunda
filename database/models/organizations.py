from database.base_model import SQLAlchemyModel
from sqlalchemy import Column, Integer, String, ForeignKey
from database.models.buildings import BuildingModel


class OrganizationModel(SQLAlchemyModel):
    __tablename__ = "organizations"
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    building_id = Column(Integer, ForeignKey(BuildingModel.id), nullable=False)
