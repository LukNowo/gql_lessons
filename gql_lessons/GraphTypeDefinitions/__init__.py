from typing import List, Union, Optional, Annotated
import strawberry as strawberryA
import typing
import strawberry
import uuid
from contextlib import asynccontextmanager
from gql_lessons.utils.Dataloaders import Loaders 

from .userGQLModel import UserGQLModel
from .mutation import Mutation
from .query import Query

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

def getLoaders(info)-> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders


from .acLessonTypeGQLModel import AcLessonTypeGQLModel
from .acSemesterGQLModel import AcSemesterGQLModel
from .acTopicGQLModel import AcTopicGQLModel
from .eventGQLModel import EventGQLModel
from .facilityGQLModel import FacilityGQLModel
from .groupGQLModel import GroupGQLModel
from .planGQLModel import PlanGQLModel
from .plannedLessonGQLModel import PlannedLessonGQLModel

from .planGQLModel import (

    #Query
    plan_by_id,
    plan_page,

    #Mutations
    plan_insert,
    plan_update,
    plan_remove
)


@strawberry.type(description="""Type for query root""")
class Query:
        
    from .plannedLessonGQLModel import (
       planned_lesson_by_id,
       planned_lesson_page,
       planned_lessons_by_event,
       planned_lessons_by_semester,
       planned_lessons_by_topic
    )
    
    planned_lesson_by_id = planned_lesson_by_id
    planned_lesson_page = planned_lesson_page
    planned_lessons_by_event = planned_lessons_by_event
    planned_lessons_by_semester = planned_lessons_by_semester
    planned_lessons_by_topic = planned_lessons_by_topic
        

    
    plan_by_id = plan_by_id     
    plan_page = plan_page

        
    
    
@strawberry.type(description="""Type for mutation root""")
class Mutation:
    
    from .plannedLessonGQLModel import (
        planned_lesson_insert,
        planned_lesson_update,
        planned_lesson_remove,

        planned_lesson_user_insert,
        planned_lesson_user_delete,

        planned_lesson_group_insert,
        planned_lesson_group_delete,

        planned_lesson_facility_insert,
        planned_lesson_facility_delete,


    )
    planned_lesson_insert = planned_lesson_insert
    planned_lesson_remove = planned_lesson_remove
    planned_lesson_update = planned_lesson_update

    plan_insert = plan_insert
    plan_update = plan_update
    plan_remove = plan_remove

    planned_lesson_user_insert = planned_lesson_user_insert
    planned_lesson_user_delete = planned_lesson_user_delete

    planned_lesson_group_insert = planned_lesson_group_insert
    planned_lesson_group_delete = planned_lesson_group_delete

    planned_lesson_facility_insert = planned_lesson_facility_insert
    planned_lesson_facility_delete = planned_lesson_facility_delete
    

schema = strawberry.federation.Schema(query=Query, types=(UserGQLModel,), mutation=Mutation)