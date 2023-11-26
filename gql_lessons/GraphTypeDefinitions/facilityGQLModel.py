from typing import List, Annotated
import asyncio
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
class FacilityGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return FacilityGQLModel(id=id)

    @strawberryA.field(description="""planned items""")

    async def planned_lessons(self, info: strawberryA.types.Info) -> List['PlannedLessonGQLModel']:

        loader = getLoaders(info).facilityplans
        rows = await loader.filter_by(facility_id=self.id)
        rowids = (row.planlesson_id for row in rows)
        # rowids = list(rowids)
        # print(rowids)
        awaitables = (PlannedLessonGQLModel.resolve_reference(info, id) for id in rowids)
        results = await asyncio.gather(*awaitables)
        return results