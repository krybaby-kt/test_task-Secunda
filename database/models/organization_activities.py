"""
Модуль модели связи организации и деятельности.
"""
from database.base_model import SQLAlchemyModel
from sqlalchemy import Column, Integer, ForeignKey
from database.models.organizations import OrganizationModel
from database.models.activities import ActivityModel


class OrganizationActivityModel(SQLAlchemyModel):
    __tablename__ = "organization_activities"
    id = Column(Integer, unique=True, primary_key=True)
    organization_id = Column(Integer, ForeignKey(OrganizationModel.id), nullable=False)
    activity_id = Column(Integer, ForeignKey(ActivityModel.id), nullable=False)
