from typing import List, Union, Annotated
from unittest import result
import strawberry as strawberryA
from contextlib import asynccontextmanager
import datetime

AcSemesterGQLModel= Annotated["AcSemesterGQLModel",strawberryA.lazy(".acSemesterGQLModel")]
PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel",strawberryA.lazy(".plannedLessonGQLModel")]

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

def asyncSessionMakerFromInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    return asyncSessionMaker

def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a study plan for timetable creation""",
)
class PlanGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).psps
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestap""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""planned lessons""")
    async def lessons(self, info: strawberryA.types.Info) -> List["PlannedLessonGQLModel"]:
        from .plannedLessonGQLModel import PlannedLessonGQLModel
        loader = getLoaders(info).plans
        result = await loader.filter_by(plan_id=self.id)
        return result
    
    @strawberryA.field(description="""acredited semester""")
    async def semester(self, info: strawberryA.types.Info) -> Union["AcSemesterGQLModel", None]:
        from .acSemesterGQLModel import AcSemesterGQLModel
        result = await AcSemesterGQLModel.resolve_reference(id=self.semester_id)
        return result

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from gql_lessons.GraphResolvers import (
    resolvePlannedLessonBySemester,
    resolvePlannedLessonByTopic,
    resolvePlannedLessonByEvent,
)


@strawberryA.field(description="""just a check""")
async def say_hello(
    self, info: strawberryA.types.Info, id: strawberryA.ID
) -> Union[str, None]:
    result = f"Hello {id}"
    return result

@strawberryA.field(description="""Planned lesson by its id""")
async def plan_by_id(
    self, info: strawberryA.types.Info, id: strawberryA.ID
) -> Union[PlanGQLModel, None]:
    result = await PlanGQLModel.resolve_reference(info, id)
    return result

@strawberryA.field(description="""Planned lesson paged""")
async def plan_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
) -> List[PlanGQLModel]:
    loader = getLoaders(info).psps
    result = await loader.page(skip, limit)
    return result
