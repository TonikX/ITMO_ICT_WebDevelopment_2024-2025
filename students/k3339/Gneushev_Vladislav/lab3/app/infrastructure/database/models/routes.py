from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base


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
