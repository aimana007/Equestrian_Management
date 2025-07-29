from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.data.database import Base


class Rider(Base):
    __tablename__ = "riders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    age = Column(Integer)


class Horse(Base):
    __tablename__ = "horses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    age = Column(Integer)


class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("riders.id"))
    horse_id = Column(Integer, ForeignKey("horses.id"))
    event_name = Column(String)
    score = Column(Integer, default=0)

    rider = relationship("Rider")
    horse = relationship("Horse")
