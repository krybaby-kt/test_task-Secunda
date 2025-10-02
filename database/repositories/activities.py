from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock

from database.models.activities import ActivityModel


class ActivityTool(AsyncBaseIdSQLAlchemyCRUD):
    model = ActivityModel
    field_id = "id"
    lock: Lock = Lock()
