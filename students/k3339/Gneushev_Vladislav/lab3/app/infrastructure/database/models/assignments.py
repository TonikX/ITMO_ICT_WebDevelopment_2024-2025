from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped

from .base import Base
from .buses import BusDB
from .drivers import DriverDB
from .routes import RouteDB


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
