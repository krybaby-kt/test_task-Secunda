from database.base_model import SQLAlchemyModel
from sqlalchemy import Column, Integer, String, ForeignKey
from database.models.organizations import OrganizationModel


class PhoneNumberModel(SQLAlchemyModel):
    __tablename__ = "phone_numbers"
    id = Column(Integer, unique=True, primary_key=True)
    organization_id = Column(Integer, ForeignKey(OrganizationModel.id), nullable=False)
    phone_number = Column(String, nullable=False)
