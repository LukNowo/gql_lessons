from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

import strawberry
import datetime
import typing

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from gql_lessons.DBDefinitions import (
    BaseModel,
    PlannedLessonModel,
    UserPlanModel,
    GroupPlanModel,
    FacilityPlanModel,
)

# from gql_lessons.DBDefinitions import UnavailabilityPL, UnavailabilityUser, UnavailabilityFacility
# from gql_lessons.DBDefinitions import FacilityModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

resolvePlannedLessonPage = createEntityGetter(
    PlannedLessonModel
)  # fuction. return a list
resolvePlannedLessonById = createEntityByIdGetter(PlannedLessonModel)  # single row .
resolvePlannedLessonByTopic = create1NGetter(
    PlannedLessonModel, foreignKeyName="topic_id"
)
resolvePlannedLessonBySemester = create1NGetter(
    PlannedLessonModel, foreignKeyName="semester_id"
)
resolvePlannedLessonByEvent = create1NGetter(
    PlannedLessonModel, foreignKeyName="event_id"
)
resolvePlannedLessonsByLink = create1NGetter(
    PlannedLessonModel, foreignKeyName="linkedlesson_id"
)

# intermediate data resolver
resolveUserLinksForPlannedLesson = create1NGetter(
    UserPlanModel, foreignKeyName="plannedlesson_id"
)  #
resolveGroupLinksForPlannedLesson = create1NGetter(
    GroupPlanModel, foreignKeyName="plannedlesson_id"
)
resolveFacilityLinksForPlannedLesson = create1NGetter(
    FacilityPlanModel, foreignKeyName="plannedlesson_id"
)
# resolveEventLinksForPlannedLesson = create1NGetter(Eve)

# unavailable Plan lesson resolver
# resolveUnavailabilityPLById = createEntityByIdGetter(UnavailabilityPL)
# resolveUnavailabilityPLAll = createEntityGetter(UnavailabilityPL)
# resolverUpdateUnavailabilityPL = createUpdateResolver(UnavailabilityPL)
# resolveInsertUnavailabilityPL = createInsertResolver(UnavailabilityPL)

# unavailable User resolver
# resolveUnavailabilityUserById = createEntityByIdGetter(UnavailabilityUser)
# resolveUnavailabilityUserAll = createEntityGetter(UnavailabilityUser)
# resolverUpdateUnavailabilityUser = createUpdateResolver(UnavailabilityUser)
# resolveInsertUnavailabilityUser = createInsertResolver(UnavailabilityUser)

# unavailable Facility resolver
# resolveUnavailabilityFacilityById = createEntityByIdGetter(UnavailabilityFacility)
# resolveUnavailabilityFacilityAll = createEntityGetter(UnavailabilityFacility)
# resolverUpdateUnavailabilityFacility = createUpdateResolver(UnavailabilityFacility)
# resolveInsertUnavailabilityFacility = createInsertResolver(UnavailabilityFacility)

from sqlalchemy import delete, insert

async def resolveRemoveUsersFromPlan(asyncSessionMaker, plan_id, usersids):
    deleteStmt = (delete(UserPlanModel)
        .where(UserPlanModel.planlesson_id==plan_id)
        .where(UserPlanModel.user_id.in_(usersids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddUsersToPlan(asyncSessionMaker, plan_id, usersids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(UserPlanModel), [{"plan_id": plan_id, "user_id": user_id} for user_id in usersids])
        await session.commit()

async def resolveRemoveGroupsFromPlan(asyncSessionMaker, plan_id, groupids):
    deleteStmt = (delete(GroupPlanModel)
        .where(GroupPlanModel.planlesson_id==plan_id)
        .where(GroupPlanModel.group_id.in_(groupids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddGroupsToPlan(asyncSessionMaker, plan_id, groupids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(GroupPlanModel), [{"plan_id": plan_id, "group_id": group_id} for group_id in groupids])
        await session.commit()

async def resolveRemoveFacilitiesFromPlan(asyncSessionMaker, plan_id, facilityids):
    deleteStmt = (delete(FacilityPlanModel)
        .where(FacilityPlanModel.planlesson_id==plan_id)
        .where(FacilityPlanModel.facility_id.in_(facilityids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddFacilitiesToPlan(asyncSessionMaker, plan_id, facilityids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(FacilityPlanModel), [{"plan_id": plan_id, "facility_id": facility_id} for facility_id in facilityids])
        await session.commit()

async def resolveRemovePlan(asyncSessionMaker, plan_id):
    deleteAStmt = delete(UserPlanModel).where(UserPlanModel.planlesson_id==plan_id)
    deleteBStmt = delete(GroupPlanModel).where(GroupPlanModel.planlesson_id==plan_id)
    deleteCStmt = delete(FacilityPlanModel).where(FacilityPlanModel.planlesson_id==plan_id)
    deleteDStmt = delete(PlannedLessonModel).where(PlannedLessonModel.id==plan_id)
    async with asyncSessionMaker() as session:
        await session.execute(deleteAStmt)
        await session.execute(deleteBStmt)
        await session.execute(deleteCStmt)
        await session.execute(deleteDStmt)
        await session.commit()

# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE
# NEW CODE



UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("GraphTypeDefinitons.userGQLModel")]


@strawberry.field(description="""Entity primary key""")
def resolve_id(self) -> uuid.UUID:
    return self.id

@strawberry.field(description="""Time of last update""")
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(description="""Name """)
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="""English name""")
def resolve_name_en(self) -> str:
    result = self.name_en if self.name_en else ""
    return result

@strawberry.field(description="""Authorization id """)
def resolve_authorization_id(self) -> uuid.UUID:
    return self.authorization_id





async def resolve_user(user_id):
    from GraphTypeDefinitions.userGQLModel import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
    return result


@strawberry.field(description="""User ID """)
async def resolve_user_id(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.user_id)



@strawberry.field(description="""Level of authorization""")
def resolve_accesslevel(self) -> int:
    return self.accesslevel


@strawberry.field(description="""Time of entity introduction""")
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created


@strawberry.field(description="""Who created entity""")
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.createdby)


@strawberry.field(description="""Who made last change""")
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby)


# answers

resolve_result_id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

# fields for mutations insert and update
resolve_insert_id = strawberry.field(graphql_type=typing.Optional[uuid.UUID], description="primary key (UUID), could be client generated", default=None)
resolve_update_id = strawberry.field(graphql_type=uuid.UUID, description="primary key (UUID), identifies object of operation")
resolve_update_lastchage = strawberry.field(graphql_type=datetime.datetime, description="timestamp of last change = TOKEN")

# fields for mutation result
resolve_cu_result_id = strawberry.field(graphql_type=uuid.UUID, description="primary key of CU operation object")
resolve_cu_result_msg = strawberry.field(graphql_type=str, description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")



def createAttributeScalarResolver(
    scalarType: None = None,
    foreignKeyName: str = None,
    description="Retrieves item by its id",
    permission_classes=()
):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description, permission_classes=permission_classes)
    async def foreignkeyScalar(
        self, info: strawberry.types.Info
    ) -> typing.Optional[scalarType]:
        # 👇 self must have an attribute, otherwise it is fail of definition
        assert hasattr(self, foreignKeyName)
        id = getattr(self, foreignKeyName, None)

        result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
        return result

    return foreignkeyScalar


def createAttributeVectorResolver(
    scalarType: None = None,
    whereFilterType: None = None,
    foreignKeyName: str = None,
    loaderLambda=lambda info: None,
    description="Retrieves items paged",
    skip: int = 0,
    limit: int = 10):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description)
    async def foreignkeyVector(
            self, info: strawberry.types.Info,
            skip: int = skip,
            limit: int = limit,
            where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        params = {foreignKeyName: self.id}
        loader = loaderLambda(info)
        assert loader is not None

        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
        return result

    return foreignkeyVector


def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None

    @strawberry.field(description=description)
    async def by_id(
            self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[scalarType]:
        result = await scalarType.resolve_reference(info=info, id=id)
        return result

    return by_id


def createRootResolver_by_page(
        scalarType: None,
        whereFilterType: None,
        loaderLambda=lambda info: None,
        description="Retrieves items paged",
        skip: int = 0,
        limit: int = 10):
    assert scalarType is not None
    assert whereFilterType is not None

    @strawberry.field(description=description)
    async def paged(
            self, info: strawberry.types.Info,
            skip: int = skip, limit: int = limit, where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf)
        return result

    return paged