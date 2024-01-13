from typing import List
import strawberry as strawberryA
import uuid

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
class EventGQLModel:

    id: uuid.UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return EventGQLModel(id=id)
    