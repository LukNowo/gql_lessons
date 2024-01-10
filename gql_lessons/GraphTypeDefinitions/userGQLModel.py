from typing import List, Annotated
import asyncio
from unittest import result
import strawberry as strawberryA

PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel",strawberryA.lazy(".plannedLessonGQLModel")]

def getLoaders(info):
    return info.context['all']

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

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz


#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,  self.id)
#         return result

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