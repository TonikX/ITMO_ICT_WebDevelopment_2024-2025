from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from starlette import status

from app.domain.entities.buses import BusType
from app.domain.entities.drivers import Driver, DriverClass
from app.presentation.api.decorators.only_admin import only_admin
from app.presentation.api.routes.assignments.schemas import GetAssignmentSchema, AddAssignmentSchema
from app.presentation.api.routes.buses.schemas import GetBusSchema, AddBusSchema, GetBusTypeSchema, AddBusTypeSchema
from app.presentation.api.routes.drivers.schemas import GetDriverSchema, AddDriverSchema, GetDriverClassSchema
from app.services.assignments import AssignmentService
from app.services.buses import BusService
from app.services.drivers import DriverService

router = APIRouter(
    prefix="/buses",
    tags=["Автобусы"],
    route_class=DishkaRoute
)


@router.get(
    "",
    summary="Получить список автобусов",
    response_model=list[GetBusSchema]
)
async def get_buses(
        bus_service: FromDishka[BusService],
):
    buses = await bus_service.get_buses()
    return [
        GetBusSchema.model_validate(bus, from_attributes=True)
        for bus in buses
    ]


@router.post(
    "",
    summary="Добавить автобус",
    response_model=GetBusSchema,
    status_code=status.HTTP_201_CREATED
)
@only_admin

async def add_bus(
        bus: AddBusSchema,
        bus_service: FromDishka[BusService],
):
    bus = await bus_service.add_bus(
        state_number=bus.state_number,
        bus_type_id=bus.bus_type_id
    )
    return GetBusSchema.model_validate(bus, from_attributes=True)


@router.delete(
    "/{bus_id}",
    summary="Удалить автобус",
    status_code=status.HTTP_204_NO_CONTENT
)
@only_admin
async def delete_bus(
        bus_id: int,
        bus_service: FromDishka[BusService],
):
    await bus_service.delete_bus(bus_id)


@router.post(
    "/types",
    summary="Добавить тип автобуса",
    response_model=GetBusTypeSchema,
)
@only_admin
async def add_bus_type(
        bus_type: AddBusTypeSchema,
        bus_service: FromDishka[BusService],
):
    bus_type = await bus_service.add_bus_type(
        BusType(
            id=None,
            name=bus_type.name,
            people_capacity=bus_type.people_capacity
        )
    )
    return GetBusTypeSchema.model_validate(bus_type, from_attributes=True)


@router.get(
    "/types",
    summary="Получить список типов автобусов",
    response_model=list[GetBusTypeSchema]
)
async def get_bus_types(
        bus_service: FromDishka[BusService],
):
    bus_types = await bus_service.get_bus_types()
    return [
        GetBusTypeSchema.model_validate(bus_type, from_attributes=True)
        for bus_type in bus_types
    ]


@router.delete(
    "/types/{bus_type_id}",
    summary="Удалить тип автобуса",
    status_code=status.HTTP_204_NO_CONTENT
)
@only_admin
async def delete_bus_type(
        bus_type_id: int,
        bus_service: FromDishka[BusService],
):
    await bus_service.delete_bus_type(bus_type_id)
