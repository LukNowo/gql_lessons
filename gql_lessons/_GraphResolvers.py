# import strawberry
# import uuid
# import datetime
# import typing
# import logging

# from GraphTypeDefinitions.BaseGQLModel import IDType

# UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
# GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".externals")]

# @strawberry.field(description="""Entity primary key""")
# def resolve_id(self) -> IDType:
#     return self.id

# @strawberry.field(description="""Name """)
# def resolve_name(self) -> str:
#     return self.name

# @strawberry.field(description="""English name""")
# def resolve_name_en(self) -> str:
#     result = self.name_en if self.name_en else ""
#     return result

# @strawberry.field(description="""Time of last update""")
# def resolve_lastchange(self) -> datetime.datetime:
#     return self.lastchange

# @strawberry.field(description="""Time of entity introduction""")
# def resolve_created(self) -> typing.Optional[datetime.datetime]:
#     return self.created

# async def resolve_user(user_id):
#     from .externals import UserGQLModel
#     result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
#     return result
    
# @strawberry.field(description="""Who created entity""")
# async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
#     return await resolve_user(self.createdby)

# @strawberry.field(description="""Who made last change""")
# async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
#     return await resolve_user(self.changedby)

# RBACObjectGQLModel = typing.Annotated["RBACObjectGQLModel", strawberry.lazy(".externals")]
# @strawberry.field(description="""Who made last change""")
# async def resolve_rbacobject(self, info: strawberry.types.Info) -> typing.Optional[RBACObjectGQLModel]:
#     from .externals import RBACObjectGQLModel
#     result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.rbacobject)
#     return result

# resolve_result_id: IDType = strawberry.field(description="primary key of CU operation object")
# resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
# For update operation fail should be also stated when bad lastchange has been entered.""")

# from inspect import signature
# import inspect 
# from functools import wraps

# def asPage(field, *, extendedfilter=None):
#     def decorator(field):
#         print(field.__name__, field.__annotations__)
#         signatureField = signature(field)
#         return_annotation = signatureField.return_annotation

#         skipParameter = signatureField.parameters.get("skip", None)
#         skipParameterDefault = 0
#         if skipParameter:
#             skipParameterDefault = skipParameter.default

#         limitParameter = signatureField.parameters.get("limit", None)
#         limitParameterDefault = 10
#         if limitParameter:
#             limitParameterDefault = limitParameter.default

#         whereParameter = signatureField.parameters.get("where", None)
#         whereParameterDefault = None
#         whereParameterAnnotation = str
#         if whereParameter:
#             whereParameterDefault = whereParameter.default
#             whereParameterAnnotation = whereParameter.annotation

#         async def foreignkeyVectorSimple(
#             self, info: strawberry.types.Info,
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signature(field).return_annotation:
#             loader = await field(self, info)
#             results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorSimple.__name__ = field.__name__
#         foreignkeyVectorSimple.__doc__ = field.__doc__

#         async def foreignkeyVectorComplex(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = None, 
#             where: typing.Optional[whereParameterAnnotation] = whereParameterDefault, 
#             where: typing.Optional[str] = None, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation:
#             logging.info(f"waiting for a loader {where}")
#             wf = None if where is None else strawberry.asdict(where)
#             loader = await field(self, info, where=wf)    
#             logging.info(f"got a loader {loader}")
#             wf = None if where is None else strawberry.asdict(where)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex.__name__ = field.__name__
#         foreignkeyVectorComplex.__doc__ = field.__doc__
        
#         if return_annotation._name == "List":
#             return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
#         else:
#             raise Exception("Unable to recognize decorated function, I am sorry")

#     return decorator(field) if field else decorator

# def asForeignList(*, foreignKeyName: str):
#     assert foreignKeyName is not None, "foreignKeyName must be defined"
#     def decorator(field):
#         print(field.__name__, field.__annotations__)
#         signatureField = signature(field)
#         return_annotation = signatureField.return_annotation

#         skipParameter = signatureField.parameters.get("skip", None)
#         skipParameterDefault = skipParameter.default if skipParameter else 0

#         limitParameter = signatureField.parameters.get("limit", None)
#         limitParameterDefault = limitParameter.default if limitParameter else 10

#         whereParameter = signatureField.parameters.get("where", None)
#         whereParameterDefault = whereParameter.default if whereParameter else None
#         whereParameterAnnotation = whereParameter.annotation if whereParameter else str

#         async def foreignkeyVectorSimple(
#             self, info: strawberry.types.Info,
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signature(field).return_annotation:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
#             if inspect.isawaitable(loader):
#                 loader = await loader
#             results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorSimple.__name__ = field.__name__
#         foreignkeyVectorSimple.__doc__ = field.__doc__
#         foreignkeyVectorSimple.__module__ = field.__module__

#         async def foreignkeyVectorComplex(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = whereParameterDefault, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
#             if inspect.isawaitable(loader):
#                 loader = await loader
            
#             wf = None if where is None else strawberry.asdict(where)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex.__name__ = field.__name__
#         foreignkeyVectorComplex.__doc__ = field.__doc__
#         foreignkeyVectorComplex.__module__ = field.__module__

#         async def foreignkeyVectorComplex2(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = whereParameterDefault, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation: #typing.List[str]:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
            
#             wf = None if where is None else strawberry.asdict(where)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex2.__module__ = field.__module__
#         if return_annotation._name == "List":
#             return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
#         else:
#             raise Exception("Unable to recognize decorated function, I am sorry")

#     return decorator

# def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
#     assert scalarType is not None
#     @strawberry.field(description=description)
#     async def by_id(
#         self, info: strawberry.types.Info, id: IDType
#     ) -> typing.Optional[scalarType]:
#         result = await scalarType.resolve_reference(info=info, id=id)
#         return result
#     return by_id

# def createRootResolver_by_page(
#     scalarType: None, 
#     whereFilterType: None,
#     loaderLambda = lambda info: None, 
#     description="Retrieves items paged", 
#     skip: int=0, 
#     limit: int=10,
#     order_by: typing.Optional[str] = None,
#     desc: typing.Optional[bool] = None):

#     assert scalarType is not None
#     assert whereFilterType is not None
    
#     @strawberry.field(description=description)
#     async def paged(
#         self, info: strawberry.types.Info, 
#         skip: int=skip, limit: int=limit, where: typing.Optional[whereFilterType] = None
#     ) -> typing.List[scalarType]:
#         loader = loaderLambda(info)
#         assert loader is not None
#         wf = None if where is None else strawberry.asdict(where)
#         result = await loader.page(skip=skip, limit=limit, where=wf, orderby=order_by, desc=desc)
#         return result
#     return paged

# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE
# # OLD   CODE

# from ast import Call
# from typing import Coroutine, Callable, Awaitable, Union, List
# import uuid
# from sqlalchemy.future import select
# from sqlalchemy.orm import selectinload, joinedload
# from sqlalchemy.ext.asyncio import AsyncSession

# from uoishelpers.resolvers import (
#     create1NGetter,
#     createEntityByIdGetter,
#     createEntityGetter,
#     createInsertResolver,
#     createUpdateResolver,
# )
# from uoishelpers.resolvers import putSingleEntityToDb

# from gql_lessons.DBDefinitions import (
#     BaseModel,
#     PlannedLessonModel,
#     UserPlanModel,
#     GroupPlanModel,
#     FacilityPlanModel,
# )

# from gql_lessons.DBDefinitions import UnavailabilityPL, UnavailabilityUser, UnavailabilityFacility
# from gql_lessons.DBDefinitions import FacilityModel

# ##########################################################################################################################

# #zde si naimportujte sve SQLAlchemy modely

# ##########################################################################################################################


# ##########################################################################################################################

# #zde definujte sve resolvery s pomoci funkci vyse
# #tyto pouzijete v GraphTypeDefinitions

# ##########################################################################################################################

# # Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

# resolvePlannedLessonPage = createEntityGetter(
#     PlannedLessonModel
# )  # fuction. return a list
# resolvePlannedLessonById = createEntityByIdGetter(PlannedLessonModel)  # single row .
# resolvePlannedLessonByTopic = create1NGetter(
#     PlannedLessonModel, foreignKeyName="topic_id"
# )
# resolvePlannedLessonBySemester = create1NGetter(
#     PlannedLessonModel, foreignKeyName="semester_id"
# )
# resolvePlannedLessonByEvent = create1NGetter(
#     PlannedLessonModel, foreignKeyName="event_id"
# )
# resolvePlannedLessonsByLink = create1NGetter(
#     PlannedLessonModel, foreignKeyName="linkedlesson_id"
# )

# intermediate data resolver
# resolveUserLinksForPlannedLesson = create1NGetter(
#     UserPlanModel, foreignKeyName="plannedlesson_id"
# )  #
# resolveGroupLinksForPlannedLesson = create1NGetter(
#     GroupPlanModel, foreignKeyName="plannedlesson_id"
# )
# resolveFacilityLinksForPlannedLesson = create1NGetter(
#     FacilityPlanModel, foreignKeyName="plannedlesson_id"
# )
# resolveEventLinksForPlannedLesson = create1NGetter(Eve)

# # unavailable Plan lesson resolver
# # resolveUnavailabilityPLById = createEntityByIdGetter(UnavailabilityPL)
# # resolveUnavailabilityPLAll = createEntityGetter(UnavailabilityPL)
# # resolverUpdateUnavailabilityPL = createUpdateResolver(UnavailabilityPL)
# # resolveInsertUnavailabilityPL = createInsertResolver(UnavailabilityPL)

# # unavailable User resolver
# # resolveUnavailabilityUserById = createEntityByIdGetter(UnavailabilityUser)
# # resolveUnavailabilityUserAll = createEntityGetter(UnavailabilityUser)
# # resolverUpdateUnavailabilityUser = createUpdateResolver(UnavailabilityUser)
# # resolveInsertUnavailabilityUser = createInsertResolver(UnavailabilityUser)

# # unavailable Facility resolver
# # resolveUnavailabilityFacilityById = createEntityByIdGetter(UnavailabilityFacility)
# # resolveUnavailabilityFacilityAll = createEntityGetter(UnavailabilityFacility)
# # resolverUpdateUnavailabilityFacility = createUpdateResolver(UnavailabilityFacility)
# # resolveInsertUnavailabilityFacility = createInsertResolver(UnavailabilityFacility)

# from sqlalchemy import delete, insert

# async def resolveRemoveUsersFromPlan(asyncSessionMaker, plan_id, usersids):
#     deleteStmt = (delete(UserPlanModel)
#         .where(UserPlanModel.planlesson_id==plan_id)
#         .where(UserPlanModel.user_id.in_(usersids)))
#     async with asyncSessionMaker() as session:
#         await session.execute(deleteStmt)
#         await session.commit()

# async def resolveAddUsersToPlan(asyncSessionMaker, plan_id, usersids):
#     async with asyncSessionMaker() as session:
#         await session.execute(insert(UserPlanModel), [{"plan_id": plan_id, "user_id": user_id} for user_id in usersids])
#         await session.commit()

# async def resolveRemoveGroupsFromPlan(asyncSessionMaker, plan_id, groupids):
#     deleteStmt = (delete(GroupPlanModel)
#         .where(GroupPlanModel.planlesson_id==plan_id)
#         .where(GroupPlanModel.group_id.in_(groupids)))
#     async with asyncSessionMaker() as session:
#         await session.execute(deleteStmt)
#         await session.commit()

# async def resolveAddGroupsToPlan(asyncSessionMaker, plan_id, groupids):
#     async with asyncSessionMaker() as session:
#         await session.execute(insert(GroupPlanModel), [{"plan_id": plan_id, "group_id": group_id} for group_id in groupids])
#         await session.commit()

# async def resolveRemoveFacilitiesFromPlan(asyncSessionMaker, plan_id, facilityids):
#     deleteStmt = (delete(FacilityPlanModel)
#         .where(FacilityPlanModel.planlesson_id==plan_id)
#         .where(FacilityPlanModel.facility_id.in_(facilityids)))
#     async with asyncSessionMaker() as session:
#         await session.execute(deleteStmt)
#         await session.commit()

# async def resolveAddFacilitiesToPlan(asyncSessionMaker, plan_id, facilityids):
#     async with asyncSessionMaker() as session:
#         await session.execute(insert(FacilityPlanModel), [{"plan_id": plan_id, "facility_id": facility_id} for facility_id in facilityids])
#         await session.commit()

# async def resolveRemovePlan(asyncSessionMaker, plan_id):
#     deleteAStmt = delete(UserPlanModel).where(UserPlanModel.planlesson_id==plan_id)
#     deleteBStmt = delete(GroupPlanModel).where(GroupPlanModel.planlesson_id==plan_id)
#     deleteCStmt = delete(FacilityPlanModel).where(FacilityPlanModel.planlesson_id==plan_id)
#     deleteDStmt = delete(PlannedLessonModel).where(PlannedLessonModel.id==plan_id)
#     async with asyncSessionMaker() as session:
#         await session.execute(deleteAStmt)
#         await session.execute(deleteBStmt)
#         await session.execute(deleteCStmt)
#         await session.execute(deleteDStmt)
#         await session.commit()
