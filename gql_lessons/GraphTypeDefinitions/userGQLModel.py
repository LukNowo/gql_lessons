from typing import List, Annotated
import asyncio
from unittest import result
import strawberry as strawberryA
import uuid

PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel",strawberryA.lazy(".plannedLessonGQLModel")]

def getLoaders(info):
    return info.context['all']

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: uuid.UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return UserGQLModel(id=id)
    
    @strawberryA.field(description="""planned items""")
    async def planned_lessons(self, info: strawberryA.types.Info) -> List['PlannedLessonGQLModel']:
        from .plannedLessonGQLModel import PlannedLessonGQLModel

        loader = getLoaders(info).userplans
        rows = await loader.filter_by(user_id=self.id)
        rowids = (row.planlesson_id for row in rows)

        awaitables = (PlannedLessonGQLModel.resolve_reference(info, id) for id in rowids)
        results = await asyncio.gather(*awaitables)
        return filter(lambda item: item is not None, results)

