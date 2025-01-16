### Назначения водителей на маршруты
```
class EndAssignmentReason(str, Enum):
    driver_ill = "driver_ill"
    bus_broken = "bus_broken"
    route_canceled = "route_canceled"
    bus_write_off = "bus_write_off"
    other = "other"


class DayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


@dataclass
class DriverAssignment(Entity):
    id: int | None
    from_date: datetime
    to_date: datetime | None
    end_reason: EndAssignmentReason | None
    day_of_week: DayOfWeek
    driver: Driver
    route: Route
    bus: Bus
```

### Водители, классы водителей и их зарплаты
```
@dataclass
class DriverClass(Entity):
    id: int | None
    name: str

    def __hash__(self):
        return hash(self.id)


@dataclass
class DriverSalary(Entity):
    id: int | None
    work_experience_over_months: int
    driver_class: DriverClass
    salary_rub: int


@dataclass
class Driver(Entity):
    id: int | None
    first_name: str
    last_name: str
    passport_info: str
    driver_class: DriverClass
    work_experience_months: int
    salary: DriverSalary | None = None


@dataclass
class DriverWorkSchedule(WorkSchedule):
    driver: Driver
```

### Маршруты
```
@dataclass
class Route(Entity):
    id: int | None
    name: str
    start_point_name: str
    end_point_name: str
    start_time: time
    end_time: time
    interval_seconds: int
    duration_seconds: int
    length: kilometers


@dataclass
class RouteWorkSchedule(WorkSchedule):
    route: Route
```

### Автобусы и их типы
```
@dataclass
class BusType(Entity):
    id: int | None
    name: str
    people_capacity: int


@dataclass
class Bus(Entity):
    id: int | None
    state_number: str
    bus_type: BusType
```

### Пользователи
```
@dataclass
class User(Entity):
    id: int | None
    username: str
    password_hash: str
    is_admin: bool
```


### JWT-токены
```
@dataclass
class JWTToken(Entity):
    token: str
    expires_at: datetime


@dataclass
class JWTTokenPayload(Entity):
    user_id: int
    expires_at: datetime
```