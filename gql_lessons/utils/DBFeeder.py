import datetime
from functools import cache

# from gql_workflow.DBDefinitions import BaseModel, UserModel, GroupModel, RoleTypeModel
# import the base model, when appolo sever ask your container for the first time, gql will ask
# next step define some resolver, how to use resolver in the file graptype
# check all data strcture in database if it have -- (work)
from gql_lessons.DBDefinitions import (
    FacilityPlanModel,
    GroupPlanModel,
    PlanModel,
    PlannedLessonModel,
    UserPlanModel,
)

from functools import cache

import os
import json
from uoishelpers.feeders import ImportModels
import datetime
import uuid

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
            
            if (key in ["id", "changedby", "createdby", "rbacobject"]) or ("_id" in key):
                
                if key == "outer_id":
                    json_dict[key] = value
                elif value not in ["", None]:
                    json_dict[key] = uuid.UUID(value)
                else:
                    print(key, value)

        return json_dict


    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    demoMode = os.environ.get("DEMO", "False")
    if demoMode == "False":
        dbModels = [
            FacilityPlanModel,
            GroupPlanModel,
            PlanModel,
            PlannedLessonModel,
            UserPlanModel,
            ]
    else:
        dbModels = [
            FacilityPlanModel,
            GroupPlanModel,
            PlanModel,
            PlannedLessonModel,
            UserPlanModel,
        ]
        
    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass

# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE
# OLD   CODE

from doctest import master
from functools import cache
from gql_lessons.DBDefinitions import (
    PlanModel,
    PlannedLessonModel,
    UserPlanModel,
    GroupPlanModel,
    FacilityPlanModel
)

import random
import itertools
from functools import cache


from sqlalchemy.future import select


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


###########################################################################################################################
#
# zde definujte sva systemova data
#
###########################################################################################################################


@cache
def types1():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {"id": "282e67ec-6d9e-11ed-a1eb-0242ac120002", "name": "typeA"},
        {"id": "282e6e86-6d9e-11ed-a1eb-0242ac120002", "name": "typeB"},
        {"id": "282e7002-6d9e-11ed-a1eb-0242ac120002", "name": "typeC"},
    ]
    return data


@cache
def types2():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {"id": "4b883614-6d9e-11ed-a1eb-0242ac120002", "name": "typeX"},
        {"id": "4b8838a8-6d9e-11ed-a1eb-0242ac120002", "name": "typeY"},
        {"id": "4b883a38-6d9e-11ed-a1eb-0242ac120002", "name": "typeZ"},
    ]
    return data


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

import asyncio

import os
import json
from uoishelpers.feeders import ImportModels
import datetime

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
        return json_dict


    with open("./systemdata.json", "r") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    defaultNoDemo = "False"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
        ]
    else:
        dbModels = [
            PlanModel,
            PlannedLessonModel,
            UserPlanModel,
            GroupPlanModel,
            FacilityPlanModel
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass