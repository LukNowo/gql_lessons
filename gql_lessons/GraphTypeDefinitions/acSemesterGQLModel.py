from typing import List, Annotated
import strawberry as strawberryA

PlanGQLModel = Annotated["PlanGQLModel",strawberryA.lazy(".planGQLModel")]

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
class AcSemesterGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
    
        return AcSemesterGQLModel(id=id)
    
    @strawberryA.field(description="""Plans""")
    async def plans(self, info: strawberryA.types.Info) -> List["PlanGQLModel"]:
        from .planGQLModel import PlanGQLModel
        loader = getLoaders(info).psps
        result = await loader.filter_by(semester_id=self.id)
        return result