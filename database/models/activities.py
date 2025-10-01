from database.base_model import SQLAlchemyModel
from sqlalchemy import Column, Integer, String, ForeignKey


class ActivityModel(SQLAlchemyModel):
    __tablename__ = "activities"
    id = Column(Integer, unique=True, primary_key=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
