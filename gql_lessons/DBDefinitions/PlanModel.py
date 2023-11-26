import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey,
    Column,
    DateTime,
)
from .UUID import UUIDColumn, UUIDFKey
from .BaseModel import BaseModel

class PlanModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable"""

    __tablename__ = "plans"

    id = UUIDColumn()
    # neni nadbytecne, topic_id muze byt null, pak je nutne mit semester_id, jedna-li se o akreditovanou vyuku
    semester_id = UUIDFKey(nullable=True)#Column(ForeignKey("acsemesters.id"), index=True, nullable=True)


    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)