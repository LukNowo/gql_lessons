import strawberry

@strawberry.type
class Mutation:
    
    from .plannedLessonGQLModel import planned_lesson_user_insert
    
    planned_lesson_user_insert = planned_lesson_user_insert
    
    from .plannedLessonGQLModel import planned_lesson_user_delete
    
    planned_lesson_user_delete = planned_lesson_user_delete
    
    from .plannedLessonGQLModel import planned_lesson_group_insert
    
    planned_lesson_group_insert = planned_lesson_group_insert 
    
    from .plannedLessonGQLModel import planned_lesson_group_delete
    
    planned_lesson_group_delete = planned_lesson_group_delete 
    
    from .plannedLessonGQLModel import planned_lesson_facility_insert
    
    planned_lesson_facility_insert =planned_lesson_facility_insert   
    
    from .plannedLessonGQLModel import planned_lesson_facility_delete
    
    planned_lesson_facility_delete = planned_lesson_facility_delete 

    from .plannedLessonGQLModel import planned_lesson_insert
    
    planned_lesson_insert = planned_lesson_insert   

    from .plannedLessonGQLModel import planned_lesson_update
    
    planned_lesson_update = planned_lesson_update       

    from .plannedLessonGQLModel import planned_lesson_remove
    
    planned_lesson_remove = planned_lesson_remove      
   
    pass