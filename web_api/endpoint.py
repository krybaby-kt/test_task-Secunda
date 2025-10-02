"""
Модуль для endpoint'ов FastAPI.
"""
from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from database.repositories.organizations import OrganizationTool
from database.models.organizations import OrganizationModel
from database.models.organization_activities import OrganizationActivityModel
from database.repositories.organization_activities import OrganizationActivityTool
from database.models.buildings import BuildingModel
from database.repositories.buildings import BuildingTool
from web_api.dependencies.api_key import require_api_key
from fastapi import Depends
from typing import List
from utils.radius import haversine_distance
from database.models.activities import ActivityModel
from database.repositories.activities import ActivityTool
from web_api.schematics import OrganizationInfo


router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get(
    "/get-all-organizations-by-building-id/{building_id}",
    description="Получить все организации по id здания",
    response_model=List[OrganizationInfo],
    response_model_exclude_none=True
)
async def get_all_organizations_by_building_id(
    building_id: int = Path(..., description="ID здания")
):
    """
    Возвращает список организаций, связанных с указанным зданием.
    """
    organizations: list[OrganizationModel] = await OrganizationTool.get_all_with_filters(filters=[OrganizationModel.building_id == building_id])

    return JSONResponse(
        content=[
            await OrganizationTool.get_organization_info(organization) for organization in organizations
        ]
    )


@router.get(
    "/get-all-organizations-by-activity-id/{activity_id}",
    description="Получить все организации по id деятельности",
    response_model=List[OrganizationInfo],
    response_model_exclude_none=True
)
async def get_all_organizations_by_activity_id(
    activity_id: int = Path(..., description="ID деятельности")
):
    """
    Возвращает список организаций, связанных с указанной деятельностью.
    """
    organization_activities: list[OrganizationActivityModel] = await OrganizationActivityTool.get_all_with_filters(filters=[OrganizationActivityModel.activity_id == activity_id])
    organizations: list[OrganizationModel] = await OrganizationTool.get_all_with_filters(filters=[OrganizationModel.id.in_([organization_activity.organization_id for organization_activity in organization_activities])])
    return JSONResponse(
        content=[
            await OrganizationTool.get_organization_info(organization) for organization in organizations
        ]
    )


@router.get(
    "/get-all-organizations-by-radius/",
    description="Получить организации в радиусе от точки на карте",
    response_model=List[OrganizationInfo],
    response_model_exclude_none=True
)
async def get_all_organizations_by_radius(
    latitude: float = Query(..., description="Широта центральной точки"),
    longitude: float = Query(..., description="Долгота центральной точки"),
    radius_km: float = Query(..., description="Радиус поиска в километрах", gt=0)
):
    """
    Возвращает список организаций, здания которых находятся в заданном радиусе от точки.
    """
    all_buildings: list[BuildingModel] = await BuildingTool.get_all()
    
    buildings_in_radius = []
    for building in all_buildings:
        distance = haversine_distance(
            latitude, longitude,
            float(building.latitude), float(building.longitude)
        )
        if distance <= radius_km:
            buildings_in_radius.append(building.id)
    
    if not buildings_in_radius:
        return JSONResponse(content=[])
    
    organizations: list[OrganizationModel] = await OrganizationTool.get_all_with_filters(
        filters=[OrganizationModel.building_id.in_(buildings_in_radius)]
    )
    
    return JSONResponse(
        content=[
            await OrganizationTool.get_organization_info(organization) for organization in organizations
        ]
    )


@router.get(
    "/get-all-organizations-by-bounding-box/",
    description="Получить организации в прямоугольной области на карте",
    response_model=List[OrganizationInfo],
    response_model_exclude_none=True
)
async def get_all_organizations_by_bounding_box(
    min_latitude: float = Query(..., description="Минимальная широта (юг)"),
    max_latitude: float = Query(..., description="Максимальная широта (север)"),
    min_longitude: float = Query(..., description="Минимальная долгота (запад)"),
    max_longitude: float = Query(..., description="Максимальная долгота (восток)")
):
    """
    Возвращает список организаций, здания которых находятся в прямоугольной области.
    """
    buildings: list[BuildingModel] = await BuildingTool.get_all_with_filters(
        filters=[
            BuildingModel.latitude >= min_latitude,
            BuildingModel.latitude <= max_latitude,
            BuildingModel.longitude >= min_longitude,
            BuildingModel.longitude <= max_longitude
        ]
    )
    
    if not buildings:
        return JSONResponse(content=[])
    
    building_ids = [building.id for building in buildings]
    
    organizations: list[OrganizationModel] = await OrganizationTool.get_all_with_filters(
        filters=[OrganizationModel.building_id.in_(building_ids)]
    )
    
    return JSONResponse(
        content=[
            await OrganizationTool.get_organization_info(organization) for organization in organizations
        ]
    )


@router.get(
    "/get-organization-by-id/{organization_id}",
    description="Получить организацию по её id",
    response_model=OrganizationInfo,
    response_model_exclude_none=True
)
async def get_organization_by_id(
    organization_id: int = Path(..., description="ID организации")
):
    """
    Возвращает организацию по её id.
    """
    organization: OrganizationModel = await OrganizationTool(organization_id).get()
    if organization is None:
        return JSONResponse(content=[])
    return JSONResponse(
        content=await OrganizationTool.get_organization_info(organization)
    )


@router.get(
    "/search-organizations-by-activity/{activity_name}",
    description="Поиск организаций по деятельности",
    response_model=List[OrganizationInfo],
    response_model_exclude_none=True
)
async def search_organizations_by_activity(
    activity_name: str = Path(..., description="Название деятельности")
):
    """
    Возвращает список организаций, связанных с указанной деятельностью и всеми её поддеятельностями.
    """
    activities: list[ActivityModel] = await ActivityTool.get_all_with_sub_activities(activity_name)
    organization_activities: list[OrganizationActivityModel] = await OrganizationActivityTool.get_all_with_filters(filters=[OrganizationActivityModel.activity_id.in_([activity.id for activity in activities])])
    organizations: list[OrganizationModel] = await OrganizationTool.get_all_with_filters(filters=[OrganizationModel.id.in_([organization_activity.organization_id for organization_activity in organization_activities])])
    return JSONResponse(
        content=[
            await OrganizationTool.get_organization_info(organization) for organization in organizations
        ]
    )


@router.get(
    "/search-organizations-by-name/{organization_name}",
    description="Поиск организаций по названию",
    response_model=List[OrganizationInfo],
    response_model_exclude_none=True
)
async def search_organizations_by_name(
    organization_name: str = Path(..., description="Название организации")
):
    """
    Возвращает список организаций, названия которых содержат указанную подстроку.
    """
    organizations: list[OrganizationModel] = await OrganizationTool.get_all_with_filters(filters=[OrganizationModel.name.ilike(f"%{organization_name}%")])
    return JSONResponse(
        content=[
            await OrganizationTool.get_organization_info(organization) for organization in organizations
        ]
    )
