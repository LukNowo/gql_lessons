import pytest
import uuid
from .gt_utils import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest
)


test_reference_plan_lesson = createResolveReferenceTest(
    tableName="plan_lessons",
    gqltype="PlannedLessonGQLModel",
    attributeNames=["id"],
)
test_query_form_by_id = createByIdTest(
    tableName="plan_lessons", queryEndpoint="plannedLessonById"
)
test_query_form_page = createPageTest(
    tableName="plan_lessons", queryEndpoint="plannedLessonPage"
)


# @pytest.mark.asyncio
# async def test_document_mutation():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)

#     name = "Pytest"
#     description = "Pytest description"

#     query = """
#             mutation(
#                 $name: String!
#                 $description: String!
#                 $collectionId: UUID!
#                 $type: String!
#                 $language: String!
#                 ) {
#                 operation: documentInsert(
#                     document: {
#                         name: $name
#                         description: $description
#                     },
#                     collectionId: $collectionId,
#                     type: $type,
#                     language: $language
#                 ){
#                     msg
#                     entity: document {
#                         id
#                         name
#                         lastchange
#                     }
#                 }
#             }
#         """

#     context_value = await createContext(async_session_maker)
#     variable_values = {
#         "name": name,
#         "description": description,
#         "collectionId": "7b022985-a416-49f4-b485-3d6f7d522d94", #"c9895381-5370-4261-bd5b-13fd671189f9",
#         "type": "pdf",
#         "language": "Czech",
#     }

#     resp = await schema.execute(
#         query, context_value=context_value, variable_values=variable_values
#     )

#     print(resp, flush=True)
#     assert resp.errors is None
#     data = resp.data["operation"]
#     assert data["msg"] == "Ok"
#     data = data["entity"]
#     assert data["name"] == name

#     id = data["id"]
#     lastchange = data["lastchange"]

#     name = "Pytest new name"
#     query = """
#             mutation(
#                 $id: UUID!,
#                 $lastchange: DateTime!
#                 $name: String!
#                 ) {
#                 operation: documentUpdate(document: {
#                 id: $id,
#                 lastchange: $lastchange
#                 name: $name
#             }){
#                 id
#                 msg
#                 entity: document {
#                     id
#                     name
#                     lastchange
#                 }
#             }
#             }
#         """

#     context_value = await createContext(async_session_maker)
#     variable_values = {"id": id, "name": name, "lastchange": lastchange}
#     resp = await schema.execute(
#         query, context_value=context_value, variable_values=variable_values
#     )
#     assert resp.errors is None

#     data = resp.data["operation"]
#     assert data["msg"] == "Ok"
#     data = data["entity"]
#     assert data["name"] == name

    