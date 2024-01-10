from typing import List, Union, Optional
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager


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

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################



schema = strawberryA.federation.Schema(query=Query, types=(UserGQLModel,), mutation=Mutation)