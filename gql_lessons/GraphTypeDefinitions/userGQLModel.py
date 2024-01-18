from typing import List, Annotated, Optional
import asyncio
from unittest import result
import strawberry as strawberryA
import uuid
from gql_lessons.utils.Dataloaders import Loaders
from contextlib import asynccontextmanager
import datetime

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

def getLoaders(info)-> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a planned lesson for timetable creation""",
)

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    #id: uuid.UUID = strawberryA.federation.field(external=True)

    # @classmethod
    # async def resolve_reference(cls, id: uuid.UUID):
    #     return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz
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
                    cls._strawberry_definition
                )  # some version of strawberry changed :(
        return result
    
    @strawberryA.field(description="""planned items""")
    async def planned_lessons(self, info: strawberryA.types.Info) -> List['PlannedLessonGQLModel']:
        from .plannedLessonGQLModel import PlannedLessonGQLModel
        loader = getLoaders(info).userplans
        rows = await loader.filter_by(user_id=self.id)
        rowids = (row.planlesson_id for row in rows)
        # rowids = list(rowids)
        # print(rowids)
        awaitables = (PlannedLessonGQLModel.resolve_reference(info, id) for id in rowids)
        results = await asyncio.gather(*awaitables)
        return filter(lambda item: item is not None, results)
    
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
class UserInsertGQLModel:
    name: Optional[str] = None
    name_en: Optional[str] = ""
    type_id: Optional[uuid.UUID] = None

@strawberryA.input
class UserUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[uuid.UUID] = None
    
@strawberryA.type
class UserResultGQLModel:
    id: strawberryA.ID = strawberryA.field(default=None, description="primary key value")
    msg: str = None

    @strawberryA.field(description="""Result of plan operation""")
    async def plan(self, info: strawberryA.types.Info) -> Optional[UserGQLModel]:
        result = await UserGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input
class UserDeleteGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID
    plan_id: Optional[uuid.UUID] = None
    
#############################################################
#
# Queries
#
#############################################################

@strawberryA.field(description="""Finds a user by its id""")
async def user_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Optional[UserGQLModel]:
        result = await UserGQLModel.resolve_reference(info=info,  id=id)
        return result

@strawberryA.field(description="""Page of users""")
async def plan_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[UserGQLModel]:
        loader = getLoaders(info).users
        result = await loader.page(skip, limit)
        return result

#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,  self.id)
#         return result

    