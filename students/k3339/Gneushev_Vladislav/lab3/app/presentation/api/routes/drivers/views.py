from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

from app.domain.entities.drivers import Driver, DriverClass
from app.presentation.api.decorators.only_admin import only_admin
from app.presentation.api.routes.drivers.schemas import GetDriverSchema, AddDriverSchema, GetDriverClassSchema, \
    AddDriverClassSchema, GetWorkScheduleSchema, DriverClassesCountSchema, ClassDriversCountSchema
from app.services.drivers import DriverService

router = APIRouter(
    prefix="/drivers",
    tags=["Водители"],
    route_class=DishkaRoute
)


@router.get(
    "",
    summary="Получить список водителей",
    response_model=list[GetDriverSchema]
)
async def get_drivers(
        driver_service: FromDishka[DriverService],
):
    drivers = await driver_service.get_drivers()
    return [
        GetDriverSchema(
            id=driver.id,
            first_name=driver.first_name,
            last_name=driver.last_name,
            passport_info=driver.passport_info,
            driver_class=GetDriverClassSchema.model_validate(driver.driver_class, from_attributes=True),
            work_experience_months=driver.work_experience_months,
            salary_rub=driver.salary.salary_rub if driver.salary else None
        )
        for driver in drivers
    ]


@router.post(
    "",
    summary="Добавить водителя",
    response_model=GetDriverSchema,
    status_code=status.HTTP_201_CREATED
)
@only_admin
async def add_driver(
        driver: AddDriverSchema,
        driver_service: FromDishka[DriverService],
):
    driver = await driver_service.add_driver(
        Driver(
            id=None,
            driver_class=DriverClass(
                id=None,
                name=driver.driver_class_name
            ),
            first_name=driver.first_name,
            last_name=driver.last_name,
            passport_info=driver.passport_info,
            work_experience_months=driver.work_experience_months
        )
    )
    return GetDriverSchema(
        id=driver.id,
        first_name=driver.first_name,
        last_name=driver.last_name,
        passport_info=driver.passport_info,
        driver_class=GetDriverClassSchema.model_validate(driver.driver_class, from_attributes=True),
        work_experience_months=driver.work_experience_months,
        salary_rub=driver.salary.salary_rub if driver.salary else None
    )


@router.delete(
    "/{driver_id}",
    summary="Удалить водителя",
    status_code=status.HTTP_204_NO_CONTENT
)
@only_admin
async def delete_driver(
        driver_id: int,
        driver_service: FromDishka[DriverService],
):
    await driver_service.delete_driver(driver_id)


@router.get(
    "/classes",
    summary="Получить список классов водителей",
    response_model=list[GetDriverClassSchema]
)
async def get_driver_classes(
        driver_service: FromDishka[DriverService],
):
    driver_classes = await driver_service.get_driver_classes()
    return [
        GetDriverClassSchema.model_validate(driver_class, from_attributes=True)
        for driver_class in driver_classes
    ]


@router.post(
    "/classes",
    summary="Добавить класс водителя",
    response_model=GetDriverClassSchema,
    status_code=status.HTTP_201_CREATED
)
@only_admin
async def add_driver_class(
        driver_class: AddDriverClassSchema,
        driver_service: FromDishka[DriverService],
):
    driver_class = await driver_service.add_driver_class(
        DriverClass(
            id=None,
            name=driver_class.name
        )
    )
    return GetDriverClassSchema.model_validate(driver_class, from_attributes=True)


@router.delete(
    "/classes/{driver_class_id}",
    summary="Удалить класс водителя",
    status_code=status.HTTP_204_NO_CONTENT
)
@only_admin
async def delete_driver_class(
        driver_class_id: int,
        driver_service: FromDishka[DriverService],
):
    await driver_service.delete_driver_class(driver_class_id)


@router.get(
    "/{driver_id}/work_schedule",
    summary="Получить график работы водителя",
    response_model=GetWorkScheduleSchema
)
async def get_driver_work_schedule(
        driver_id: int,
        driver_service: FromDishka[DriverService],
):
    work_schedule = await driver_service.get_driver_work_schedule(driver_id)
    return GetWorkScheduleSchema.model_validate(work_schedule, from_attributes=True)


@router.get(
    "/classes/count",
    summary="Получить количество водителей в каждом классе",
    response_model=DriverClassesCountSchema
)
async def get_driver_classes_count(
        driver_service: FromDishka[DriverService],
):
    driver_classes_count = await driver_service.get_driver_classes_count()
    return DriverClassesCountSchema(
        driver_classes=[
            ClassDriversCountSchema(
                driver_class=GetDriverClassSchema.model_validate(driver_class, from_attributes=True),
                count=drivers_count
            )
            for driver_class, drivers_count in driver_classes_count.items()
        ]
    )
