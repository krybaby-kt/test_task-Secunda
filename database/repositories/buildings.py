from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock

from database.models.buildings import BuildingModel


class BuildingTool(AsyncBaseIdSQLAlchemyCRUD):
    model = BuildingModel
    field_id = "id"
    lock: Lock = Lock()
