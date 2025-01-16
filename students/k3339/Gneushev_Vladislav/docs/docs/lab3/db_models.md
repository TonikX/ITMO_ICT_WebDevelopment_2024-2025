### Назначения водителей на маршруты
```
class DriverAssignmentDB(Base):
    __tablename__ = 'driver_assignments'
    id = Column(Integer, primary_key=True)
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=True)
    end_reason = Column(String(32), nullable=True)
    driver_id = Column(
        Integer,
        ForeignKey(
            "drivers.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    route_id = Column(
        Integer,
        ForeignKey(
            "routes.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    bus_id = Column(
        Integer,
        ForeignKey(
            "buses.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    day_of_week = Column(String(10), nullable=False)

    driver: Mapped[DriverDB] = relationship('DriverDB', back_populates='assignments', lazy='joined')
    route: Mapped[RouteDB] = relationship('RouteDB', back_populates='assignments', lazy='joined')
    bus: Mapped[BusDB] = relationship('BusDB', back_populates='assignments', lazy='joined')
```

### Водители, классы водителей и их зарплаты
```
class DriverClassDB(Base):
    __tablename__ = 'driver_classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    drivers = relationship('DriverDB', back_populates='driver_class')


class DriverSalaryDB(Base):
    __tablename__ = 'driver_salaries'
    id = Column(Integer, primary_key=True)
    work_experience_over_months = Column(Integer, nullable=False)
    driver_class_id = Column(
        Integer,
        ForeignKey(
            "driver_classes.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    salary_rub = Column(Integer, nullable=False)

    driver_class: Mapped[DriverClassDB] = relationship('DriverClassDB', lazy='joined')


class DriverDB(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    passport_info = Column(String(10), nullable=False)
    driver_class_id = Column(
        Integer,
        ForeignKey(
            "driver_classes.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    work_experience_months = Column(Integer, nullable=False)

    driver_class: Mapped[DriverClassDB] = relationship('DriverClassDB', back_populates='drivers', lazy='joined')
    assignments = relationship('DriverAssignmentDB', back_populates='driver', lazy='joined')
```

### Маршруты
```
class RouteDB(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    start_point_name = Column(String(32), nullable=False)
    end_point_name = Column(String(32), nullable=False)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)
    interval_seconds = Column(Integer, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    length_km = Column(Integer, nullable=False)

    assignments = relationship('DriverAssignmentDB', back_populates='route')
```

### Автобусы и их типы
```
class BusTypeDB(Base):
    __tablename__ = 'bus_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    people_capacity = Column(Integer, nullable=False)

    buses = relationship('BusDB', back_populates='bus_type')


class BusDB(Base):
    __tablename__ = 'buses'
    id = Column(Integer, primary_key=True)
    state_number = Column(String(32), nullable=False)
    bus_type_id = Column(
        Integer,
        ForeignKey(
            "bus_types.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    bus_type: Mapped[BusTypeDB] = relationship('BusTypeDB', back_populates='buses', lazy='joined')
    assignments = relationship('DriverAssignmentDB', back_populates='bus')
```

### Пользователи
```
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    is_admin = Column(Boolean, nullable=False)
```