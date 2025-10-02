from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock

from database.models.organization_activities import OrganizationActivityModel


class OrganizationActivityTool(AsyncBaseIdSQLAlchemyCRUD):
    model = OrganizationActivityModel
    field_id = "id"
    lock: Lock = Lock()
