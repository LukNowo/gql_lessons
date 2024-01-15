import datetime
import asyncio
import logging
from sqlalchemy import select
from functools import cache
import os
import logging

from aiodataloader import DataLoader
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader


from gql_lessons.DBDefinitions import (
    PlanModel,
    PlannedLessonModel,
    UserPlanModel,
    GroupPlanModel,
    FacilityPlanModel
)


dbmodels = {
    "psps": PlanModel,
    "plans": PlannedLessonModel,
    "userplans": UserPlanModel,
    "groupplans": GroupPlanModel,
    "facilityplans": FacilityPlanModel
}


class Loaders:
    authorizations = None
    requests = None
    histories = None
    forms = None
    formtypes = None
    formcategories = None
    sections = None
    parts = None
    items = None
    itemtypes = None
    itemcategories = None
    pass


def createLoaders(asyncSessionMaker, models=dbmodels) -> Loaders:
    class Loaders:

        # @property
        # @cache
        #  def authorizations(self):
        #     return AuthorizationLoader()

        @property
        @cache
        def answers(self):
            return createIdLoader(asyncSessionMaker,PlanModel)
        
        @property
        @cache
        def questions(self):
            return createIdLoader(asyncSessionMaker, PlannedLessonModel)
        
        @property
        @cache
        def questiontypes(self):
            return createIdLoader(asyncSessionMaker, UserPlanModel)
        
        @property
        @cache
        def questionvalues(self):
            return createIdLoader(asyncSessionMaker,GroupPlanModel)
        
        @property
        @cache
        def surveys(self):
            return createIdLoader(asyncSessionMaker, FacilityPlanModel)

        
    return Loaders()


def getLoaders(info)-> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders

def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    user = context.get("user", None)
    if user is None:
        request = context.get("request", None)
        assert request is not None, "request is missing in context :("
        user = request.scope.get("user", None)
        assert user is not None, "missing user in context or in request.scope"
    logging.debug("getUserFromInfo", user)
    return user



async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
   
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache