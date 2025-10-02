"""
Модуль репозитория организации.
"""
from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock

from database.models.organizations import OrganizationModel

from database.repositories.buildings import BuildingTool
from database.models.buildings import BuildingModel
from database.repositories.phone_numbers import PhoneNumberTool
from database.models.phone_numbers import PhoneNumberModel
from database.repositories.activities import ActivityTool
from database.models.activities import ActivityModel
from database.repositories.organization_activities import OrganizationActivityTool
from database.models.organization_activities import OrganizationActivityModel


class OrganizationTool(AsyncBaseIdSQLAlchemyCRUD):
    model = OrganizationModel
    field_id = "id"
    lock: Lock = Lock()

    @staticmethod
    async def get_organization_info(organization: OrganizationModel) -> dict:
        """
        Получает информацию о организации.
        """
        phone_numbers: list[PhoneNumberModel] = await PhoneNumberTool.get_all_with_filters(filters=[PhoneNumberModel.organization_id == organization.id])
        building: BuildingModel = await BuildingTool(organization.building_id).get()
        organization_activities: list[OrganizationActivityModel] = await OrganizationActivityTool.get_all_with_filters(filters=[OrganizationActivityModel.organization_id == organization.id])
        activities: list[ActivityModel] = await ActivityTool.get_all_with_filters(filters=[ActivityModel.id.in_([organization_activity.activity_id for organization_activity in organization_activities])])

        return {
            "id": organization.id,
            "name": organization.name,
            "phone_numbers": [{"id": phone_number.id, "phone_number": phone_number.phone_number} for phone_number in phone_numbers],
            "building": {
                "id": building.id,
                "address": building.address,
                "latitude": float(building.latitude),
                "longitude": float(building.longitude)
            },
            "activities": [{"id": activity.id, "name": activity.name} for activity in activities]
        }
