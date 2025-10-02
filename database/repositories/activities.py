from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock
import asyncio

from database.models.activities import ActivityModel


class ActivityTool(AsyncBaseIdSQLAlchemyCRUD):
    model = ActivityModel
    field_id = "id"
    lock: Lock = Lock()

    @staticmethod
    async def get_all_with_sub_activities(activity_name: str) -> list[ActivityModel]:
        activities: list[ActivityModel] = await ActivityTool.get_all_with_filters(filters=[ActivityModel.name == activity_name])
        for sub_activities in await asyncio.gather(*[ActivityTool.get_all_sub_activities_by_id(activity.id) for activity in activities]):
            activities.extend(sub_activities)
        return activities

    @staticmethod
    async def get_all_sub_activities_by_id(activity_id: int) -> list[ActivityModel]:
        sub_activities: list[ActivityModel] = await ActivityTool.get_all_with_filters(filters=[ActivityModel.parent_id == activity_id])
        for sub_activities_ in await asyncio.gather(*[ActivityTool.get_all_sub_activities_by_id(sub_activity.id) for sub_activity in sub_activities]):
            sub_activities.extend(sub_activities_)
        return sub_activities
