"""
Модуль репозитория организации.
"""
from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock

from database.models.organizations import OrganizationModel


class OrganizationTool(AsyncBaseIdSQLAlchemyCRUD):
    model = OrganizationModel
    field_id = "id"
    lock: Lock = Lock()
