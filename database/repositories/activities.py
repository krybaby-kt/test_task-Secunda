from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock
import asyncio
from typing import Dict, Any

from database.models.activities import ActivityModel


class ActivityTool(AsyncBaseIdSQLAlchemyCRUD):
    model = ActivityModel
    field_id = "id"
    lock: Lock = Lock()

    @classmethod
    async def _calculate_level(cls, parent_id: int | None) -> int:
        if parent_id is None:
            return 1
        
        parent = await ActivityTool(parent_id).get()
        if parent is None:
            raise ValueError(f"Parent activity with id {parent_id} not found")
        
        return parent.level + 1

    @classmethod
    async def create(cls, data: Dict[str, Any]) -> ActivityModel:
        parent_id = data.get('parent_id')
        
        level = await cls._calculate_level(parent_id)
        
        if level > 3:
            raise ValueError(
                f"Cannot create activity: maximum nesting level is 3. "
                f"Parent activity has level {level - 1}"
            )
        
        data['level'] = level
        
        return await super().create(data)

    async def update(self, data: Dict[str, Any]) -> ActivityModel:
        if 'parent_id' in data:
            new_parent_id = data['parent_id']
            new_level = await self._calculate_level(new_parent_id)
            
            if new_level > 3:
                raise ValueError(
                    f"Cannot update activity: maximum nesting level is 3. "
                    f"New parent activity has level {new_level - 1}"
                )
            
            data['level'] = new_level
        
        return await super().update(data)

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
