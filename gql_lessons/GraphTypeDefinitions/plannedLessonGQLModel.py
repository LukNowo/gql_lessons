from typing import List, Union, Optional, Annotated, Optional
import strawberry as strawberryA
from contextlib import asynccontextmanager
import datetime



AcLessonTypeGQLModel = Annotated["AcLessonTypeGQLModel",strawberryA.lazy(".acLessonTypeGQLModel")]
AcSemesterGQLModel= Annotated["AcSemesterGQLModel",strawberryA.lazy(".acSemesterGQLModel")]
PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel",strawberryA.lazy(".plannedLessonGQLModel")]
AcTopicGQLModel = Annotated["AcTopicGQLModel",strawberryA.lazy(".acTopicGQLModel")]
EventGQLModel = Annotated["EventGQLModel",strawberryA.lazy(".eventGQLModel")]
FacilityGQLModel = Annotated["FacilityGQLModel",strawberryA.lazy(".facilityGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel",strawberryA.lazy(".groupGQLModel")]
PlanGQLModel = Annotated["PlanGQLModel",strawberryA.lazy(".planGQLModel")]
UserGQLModel = Annotated["UserGQLModel",strawberryA.lazy(".userGQLModel")]


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
    description="""Entity representing a planned lesson for timetable creation""",
)
class PlannedLessonGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # print("PlannedLessonGQLModel.resolve_reference", id)
        loader = getLoaders(info).plans
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

    @strawberryA.field(description="""primary key""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""order""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""primary key""")
    def length(self) -> Union[int, None]:
        return self.length

    @strawberryA.field(description="""type of lesson (lecture, ...)""")
    async def type(self, info) -> Optional["AcLessonTypeGQLModel"]:
        result = await AcLessonTypeGQLModel.resolve_reference(id=self.lessontype_id)
        return result

    @strawberryA.field(
        description="""planned lesson linked to (aka master planned lesson)"""
    )
    async def linked_to(
        self, info: strawberryA.types.Info
    ) -> Union["PlannedLessonGQLModel", None]:
        loader = getLoaders(info).plans
        result = None
        if self.linkedlesson_id is not None:
            result = await loader.load(self.linkedlesson_id)
        return result

    @strawberryA.field(
        description="""planned lessons linked with, even trought master, excluding self"""
    )
    async def linked_with(
        self, info: strawberryA.types.Info
    ) -> List["PlannedLessonGQLModel"]:
        loader = getLoaders(info).plans
        result1 = await loader.load(self.id)
        if self.linkedlesson_id is not None:
            result2 = await loader.filter_by(linkedlesson_id=self.id)
            result1 = [result1, *result2]
        return result1

    @strawberryA.field(description="""teachers""")
    async def users(self, info: strawberryA.types.Info) -> List["UserGQLModel"]:
        loader = getLoaders(info).userplans
        result = await loader.filter_by(planlesson_id=self.id)
        return [UserGQLModel(id=item.user_id) for item in result]

    @strawberryA.field(description="""study groups""")
    async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]:
        loader = getLoaders(info).groupplans
        result = await loader.filter_by(planlesson_id=self.id)
        return [GroupGQLModel(id=item.group_id) for item in result]

    @strawberryA.field(description="""facilities""")
    async def facilities(
        self, info: strawberryA.types.Info
    ) -> List["FacilityGQLModel"]:
        loader = getLoaders(info).facilityplans
        result = await loader.filter_by(planlesson_id=self.id)
        return [FacilityGQLModel(id=item.facility_id) for item in result]

    @strawberryA.field(description="""linked event""")
    async def event(self, info: strawberryA.types.Info) -> Union["EventGQLModel", None]:
        if self.event_id is None:
            result = None
        else:
            result = EventGQLModel(id=self.event_id)
        return result

    @strawberryA.field(description="""linked topic from accreditation""")
    async def topic(
        self, info: strawberryA.types.Info
    ) -> Union["AcTopicGQLModel", None]:
        if self.topic_id is None:
            result = None
        else:
            result = AcTopicGQLModel(id=self.topic_id)
        return result

    @strawberryA.field(
        description="""linked subject semester from program (accreditation)"""
    )
    async def semester(
        self, info: strawberryA.types.Info
    ) -> Union["AcSemesterGQLModel", None]:
        if self.semester_id is None:
            result = None
        else:
            result = AcSemesterGQLModel(id=self.semester_id)
        return result

    @strawberryA.field(
        description="""linked subject semester from program (accreditation)"""
    )
    async def plan(
        self, info: strawberryA.types.Info
    ) -> Union["PlanGQLModel", None]:
        print("PlannedLessonGQLModel.plan", self.plan_id)
        result = await PlanGQLModel.resolve_reference(info, self.plan_id)
        print("PlannedLessonGQLModel.plan", result)
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
    resolvePlannedLessonById,
    resolvePlannedLessonPage
)


@strawberryA.field(description="""Planned lesson by its id""")
async def planned_lesson_by_id(
    self, info: strawberryA.types.Info, id: strawberryA.ID
) -> Union[PlannedLessonGQLModel, None]:
    async with withInfo(info) as session:
        result = await resolvePlannedLessonById(session, id)
        return result

@strawberryA.field(description="""Planned lesson paged""")
async def planned_lesson_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
) -> List[PlannedLessonGQLModel]:
    async with withInfo(info) as session:
        result = await resolvePlannedLessonPage(session, skip, limit)
        return result

@strawberryA.field(description="""Planned lesson by its semester (subject)""")
async def planned_lessons_by_semester(
    self, info: strawberryA.types.Info, id: strawberryA.ID
) -> List[PlannedLessonGQLModel]:
    async with withInfo(info) as session:
        result = await resolvePlannedLessonBySemester(session, id)
        return result

@strawberryA.field(description="""Planned lesson by its topic""")
async def planned_lessons_by_topic(
    self, info: strawberryA.types.Info, id: strawberryA.ID
) -> List[PlannedLessonGQLModel]:
    async with withInfo(info) as session:
        result = await resolvePlannedLessonByTopic(session, id)
        return result

@strawberryA.field(description="""Planned lesson """)
async def planned_lessons_by_event(
    self, info: strawberryA.types.Info, id: strawberryA.ID
) -> List[PlannedLessonGQLModel]:
    async with withInfo(info) as session:
        result = await resolvePlannedLessonByEvent(session, id)
        return result
        
###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional

@strawberryA.input
class PlannedLessonInsertGQLModel:
    name: str = strawberryA.field(default=None, description="Name of lesson aka 'Introduction'")
    plan_id: strawberryA.ID = strawberryA.field(default=None, description="which plan contains this lesson")
    length: Optional[int] = strawberryA.field(default=2, description="how many 45min intervals")
    startproposal: Optional[datetime.datetime] = strawberryA.field(default=None, description="proposal of datetime")
    order: Optional[int] = strawberryA.field(default=1, description="order of the item in plan")

    linkedlesson_id: Optional[strawberryA.ID] =  strawberryA.field(default=None, description="id of lesson from other plan which would be teached with")
    topic_id: Optional[strawberryA.ID] = None
    lessontype_id: Optional[strawberryA.ID] = strawberryA.field(default=None, description="aka Consultation, Laboratory, ...")
    semester_id: Optional[strawberryA.ID] = strawberryA.field(default=None, description="link to semester (subject) from accreditation")
    event_id: Optional[strawberryA.ID] = strawberryA.field(default=None, description="event defining when this would be teached")
    id: Optional[strawberryA.ID]  = strawberryA.field(default=None, description="could be primary key generated by client, UUID is expected")

@strawberryA.input
class PlannedLessonUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(default=None, description="time stamp")
    id: strawberryA.ID = strawberryA.field(default=None, description="primary key value")
    order: Optional[int] = None
    name: Optional[str] = None
    length: Optional[int] = None
    startproposal: Optional[datetime.datetime] = None

    linkedlesson_id: Optional[strawberryA.ID] = None
    topic_id: Optional[strawberryA.ID] = None
    lessontype_id: Optional[strawberryA.ID] = None
    semester_id: Optional[strawberryA.ID] = None
    event_id: Optional[strawberryA.ID] = None

@strawberryA.type
class PlannedLessonResultGQLModel:
    id: Union[strawberryA.ID, None] = None
    msg: str = None

    @strawberryA.field(description="""Result of lesson operation""")
    async def lesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel, None]:
        print("lesson", self.id)
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.type
class PlanResultGQLModel:
    id: Union[strawberryA.ID, None] = None
    msg: str = None

@strawberryA.input
class PlannedLessonDeleteGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    plan_id: Optional[strawberryA.ID] = None

   # @strawberryA.field(description="""Result of lesson operation""")
   # async def plan(self, info: strawberryA.types.Info) -> Union[PlanGQLModel, None]:
   #     result = await PlanGQLModel.resolve_reference(info, self.id)
   #     return result
    
@strawberryA.input
class PlannedLessonUserInsertGQLModel:
    user_id: strawberryA.ID
    planlesson_id: strawberryA.ID
    
@strawberryA.input
class PlannedLessonUserDeleteGQLModel:
    user_id: strawberryA.ID
    planlesson_id: strawberryA.ID

@strawberryA.input
class PlannedLessonGroupInsertGQLModel:
    group_id: strawberryA.ID
    planlesson_id: strawberryA.ID
    
@strawberryA.input
class PlannedLessonGroupDeleteGQLModel:
    group_id: strawberryA.ID
    planlesson_id: strawberryA.ID

@strawberryA.input
class PlannedLessonFacilityInsertGQLModel:
    facility_id: strawberryA.ID
    planlesson_id: strawberryA.ID
    
@strawberryA.input
class PlannedLessonFacilityDeleteGQLModel:
    facility_id: strawberryA.ID
    planlesson_id: strawberryA.ID

@strawberryA.input
class PlannedLessonAssignmentGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    users: Optional[List[strawberryA.ID]] = None
    facilities: Optional[List[strawberryA.ID]] = None
    groups: Optional[List[strawberryA.ID]] = None
    
@strawberryA.type
class PlannedLessonAssignmentResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def lesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel, None]:
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result

from gql_lessons.GraphResolvers import resolveRemovePlan

# @strawberryA.mutation
# async def planned_lesson_change_assignment(self, info: strawberryA.types.Info, assignment: PlannedLessonAssignmentGQLModel) -> PlannedLessonAssignmentResultGQLModel:
#     # loader = getLoaders(info).plans
#     # row = await loader.insert(lesson)
#     if assignment.users is not None:
#         loader = getLoaders(info).userplans
#         rows = await loader.filter_by(planlesson_id=assignment.id)
#         rowids = set(list(map(lambda item: item.id, rows)))
#         inputids = set(assignment.users)
#         toAdd = inputids - rowids
#         toRemove = rowids - inputids


#     result = PlannedLessonResultGQLModel()
#     result.msg = "not implemented"
#     result.id = None
#     return result

@strawberryA.mutation(description="Assings a teacher to the planned lesson")
async def planned_lesson_user_insert(self, info: strawberryA.types.Info, userlesson: PlannedLessonUserInsertGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoaders(info).userplans
    row = await loader.insert(userlesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "ok"
    result.id = userlesson.planlesson_id
    return result

@strawberryA.mutation(description="Removes the teacher to the planned lesson")
async def planned_lesson_user_delete(self, info: strawberryA.types.Info, userlesson: PlannedLessonUserDeleteGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoaders(info).userplans
    rows = await loader.filter_by(planlesson_id=userlesson.planlesson_id, user_id=userlesson.user_id)
    row = next(rows, None)
    result = PlannedLessonResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        print(row)
        print(row.id)
        rr = await loader.delete(row.id)
        # for r in rr.all():
        #     print(r)
        result.msg = "ok"
    result.id = userlesson.planlesson_id
    print("planned_lesson_user_delete", userlesson.planlesson_id)
    return result

@strawberryA.mutation(description="Assings a group to the planned lesson")
async def planned_lesson_group_insert(self, info: strawberryA.types.Info, grouplesson: PlannedLessonGroupInsertGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoaders(info).groupplans
    row = await loader.insert(grouplesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "ok"
    result.id = row.planlesson_id
    return result

@strawberryA.mutation(description="Removes the group to the planned lesson")
async def planned_lesson_group_delete(self, info: strawberryA.types.Info, grouplesson: PlannedLessonGroupDeleteGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoaders(info).groupplans
    rows = await loader.filter_by(planlesson_id=grouplesson.planlesson_id, group_id=grouplesson.group_id)
    row = next(rows, None)
    result = PlannedLessonResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
    result.id = grouplesson.planlesson_id
        
    return result

@strawberryA.mutation(description="Assigns a facility to the planned lesson")
async def planned_lesson_facility_insert(self, info: strawberryA.types.Info, facilitylesson: PlannedLessonFacilityInsertGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoaders(info).facilityplans
    row = await loader.insert(facilitylesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "ok"
    result.id = row.planlesson_id
    return result

@strawberryA.mutation(description="Removes the facility to the planned lesson")
async def planned_lesson_facility_delete(self, info: strawberryA.types.Info, facilitylesson: PlannedLessonFacilityDeleteGQLModel) -> PlannedLessonResultGQLModel:
    resolveRemovePlan
    loader = getLoaders(info).facilityplans
    rows = await loader.filter_by(planlesson_id=facilitylesson.planlesson_id, facility_id=facilitylesson.facility_id)
    row = next(rows, None)
    result = PlannedLessonResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
    result.id = facilitylesson.planlesson_id
    return result

@strawberryA.mutation
async def planned_lesson_insert(self, info: strawberryA.types.Info, lesson: PlannedLessonInsertGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoaders(info).plans
    row = await loader.insert(lesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation
async def planned_lesson_update(self, info: strawberryA.types.Info, lesson: PlannedLessonUpdateGQLModel) -> PlannedLessonResultGQLModel:
    resolveRemovePlan
    loader = getLoaders(info).plans
    row = await loader.update(lesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "ok"
    result.id = lesson.id
    if row is None:
        result.msg = "fail"
        
    return result

@strawberryA.mutation
async def planned_lesson_remove(self, info: strawberryA.types.Info, lesson: PlannedLessonDeleteGQLModel) -> PlanResultGQLModel:
    asyncSessionMaker = asyncSessionMakerFromInfo(info)
    await resolveRemovePlan(asyncSessionMaker, lesson.id)
    result = PlanResultGQLModel()
    result.msg = "ok"
    result.id = lesson.plan_id
        
    return result
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

