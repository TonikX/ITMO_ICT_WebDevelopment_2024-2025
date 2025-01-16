from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from app.infrastructure.database.models.base import Base


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
