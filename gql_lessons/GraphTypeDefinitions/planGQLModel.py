from typing import List, Optional, Annotated
from unittest import result
import strawberry as strawberryA
from contextlib import asynccontextmanager
import datetime
import uuid

from .BaseGQLModel import BaseGQLModel
from .plannedLessonGQLModel import PlannedLessonGQLModel



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
    def getLoaders(cls, info):
        return getLoaders(info).plans
    
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        result = None
        if id is not None:
            loader = getLoaders(info=info).plan_lessons
            # print(loader, flush=True)
            if isinstance(id, str):
                id = uuid.UUID(id)
            result = await loader.load(id)
            if result is not None:
                result._type_definition = cls._type_definition  # little hack :)
                result.__strawberry_definition__ = (
                    cls._type_definition
                )  # some version of strawberry changed :(
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Timestap""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""primary key""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""order""")
    def name_en(self) -> str:
        return self.order

@strawberryA.input
class PlanInsertGQLModel:
    name: Optional[str] = None
    name_en: Optional[str] = ""
    type_id: Optional[uuid.UUID] = None

@strawberryA.input
class PlanUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[uuid.UUID] = None
    
@strawberryA.type
class PlanResultGQLModel:
    id: strawberryA.ID = strawberryA.field(default=None, description="primary key value")
    msg: str = None

    @strawberryA.field(description="""Result of plan operation""")
    async def plan(self, info: strawberryA.types.Info) -> Optional[PlanGQLModel]:
        result = await PlanGQLModel.resolve_reference(info, self.id)
        return result
    
#############################################################
#
# Queries
#
#############################################################

@strawberryA.field(description="""Finds a plan by its id""")
async def plan_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Optional[PlanGQLModel]:
        result = await PlanGQLModel.resolve_reference(info=info,  id=id)
        return result

@strawberryA.field(description="""Page of plans""")
async def plan_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[PlanGQLModel]:
        loader = getLoaders(info).plans
        result = await loader.page(skip, limit)
        return result
#from utils.DBFeeder import randomPlanData

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

@strawberryA.mutation(description="""Creates new plan""")
async def plan_insert(self, info: strawberryA.types.Info, plan: PlanInsertGQLModel) -> PlanResultGQLModel:
        loader = getLoaders(info).plans
        row = await loader.insert(plan)
        result = PlanResultGQLModel(id=row.id, msg="ok")
        return result

@strawberryA.mutation(description="""Updates the plan""")
async def plan_update(self, info: strawberryA.types.Info, plan: PlanUpdateGQLModel) -> PlanResultGQLModel:
    
        loader = getLoaders(info).plans
        row = await loader.update(plan)
        result = PlanResultGQLModel()
        result.msg = "ok"
        result.id = plan.id
        if row is None:
            result.msg = "fail"           
        return result

@strawberryA.mutation(description="""Assigns the plan to the user. """)
async def plan_assign_to(self, info: strawberryA.types.Info, plan_id: strawberryA.ID, user_id: strawberryA.ID) -> PlanResultGQLModel:
        loader = getLoaders(info).questions
        questions = await loader.filter_by(plan_id=plan_id)
        loader = getLoaders(info).answers
        for q in questions:
            exists = await loader.filter_by(question_id=q.id, user_id=user_id)
            if next(exists, None) is None:
                #user has not this particular question
                rowa = await loader.insert(None, {"question_id": q.id, "user_id": user_id})
        result = PlanResultGQLModel()
        result.msg = "ok"
        result.id = plan_id
            
        return result


# class PlanGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
#         loader = getLoaders(info).psps
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

    # @strawberryA.field(description="""primary key""")
    # def id(self) -> uuid.UUID:
    #     return self.id

    # @strawberryA.field(description="""Timestap""")
    # def lastchange(self) -> datetime.datetime:
    #     return self.lastchange
    
    # @strawberryA.field(description="""planned lessons""")
    # async def lessons(self, info: strawberryA.types.Info) -> List["PlannedLessonGQLModel"]:
    #     from .plannedLessonGQLModel import PlannedLessonGQLModel
    #     loader = getLoaders(info).plans
    #     result = await loader.filter_by(plan_id=self.id)
    #     return result
    
    # @strawberryA.field(description="""acredited semester""")
    # async def semester(self, info: strawberryA.types.Info) -> Union["AcSemesterGQLModel", None]:
    #     from .acSemesterGQLModel import AcSemesterGQLModel
    #     result = await AcSemesterGQLModel.resolve_reference(id=self.semester_id)
        return result

# ###########################################################################################################################
# #
# # zde definujte svuj Query model
# #
# ###########################################################################################################################

# from gql_lessons.GraphResolvers import (
#     resolvePlannedLessonBySemester,
#     resolvePlannedLessonByTopic,
#     resolvePlannedLessonByEvent,
# )


# @strawberryA.field(description="""Planned lesson by its id""")
# async def plan_by_id(
#     self, info: strawberryA.types.Info, id: uuid.UUID
# ) -> Union[PlanGQLModel, None]:
#     result = await PlanGQLModel.resolve_reference(info, id)
#     return result

# @strawberryA.field(description="""Planned lesson paged""")
# async def plan_page(
#     self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
# ) -> List[PlanGQLModel]:
#     loader = getLoaders(info).psps
#     result = await loader.page(skip, limit)
#     return result
