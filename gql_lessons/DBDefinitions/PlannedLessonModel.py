import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Column,
    DateTime,
)
from .UUID import UUIDColumn, UUIDFKey
from .BaseModel import BaseModel

class PlannedLessonModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable"""

    __tablename__ = "plan_lessons"

    id = UUIDColumn()
    name = Column(String)
    order = Column(Integer, default=lambda:1)
    length = Column(Integer, nullable=True)
    startproposal = Column(DateTime, nullable=True)
    plan_id = Column(ForeignKey("plans.id"), index=True, nullable=True)

    linkedlesson_id = Column(ForeignKey("plan_lessons.id"), index=True, nullable=True)
    topic_id = UUIDFKey(nullable=True)#Column(ForeignKey("actopics.id"), index=True, nullable=True)
    lessontype_id = UUIDFKey(nullable=True)#Column(ForeignKey("aclessontypes.id"), index=True)

    # neni nadbytecne, topic_id muze byt null, pak je nutne mit semester_id, jedna-li se o akreditovanou vyuku
    semester_id = UUIDFKey(nullable=True)#Column(ForeignKey("acsemesters.id"), index=True, nullable=True)
    event_id = UUIDFKey(nullable=True)#Column(ForeignKey("events.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)