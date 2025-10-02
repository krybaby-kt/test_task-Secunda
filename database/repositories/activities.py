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
        result_activities: list[ActivityModel] = []
        activities: list[ActivityModel] = await ActivityTool.get_all_with_filters(filters=[ActivityModel.name == activity_name])
        result_activities.extend(activities)

        for activity in activities:
            sub_activities: list[ActivityModel] = await ActivityTool.get_all_with_filters(filters=[ActivityModel.parent_id == activity.id])
            result_activities.extend(sub_activities)

            results = await asyncio.gather(*[ActivityTool.get_all_with_sub_activities(sub_activity.name) for sub_activity in sub_activities])
            for result in results:
                result_activities.extend(result)

        return list(set(result_activities))
