import strawberry

@strawberry.type(description="""Type for query root""")
class Query: 
    
    from .planGQLModel import plan_by_id
    
    plan_by_id = plan_by_id     
   
    from .planGQLModel import plan_page
    
    plan_page = plan_page     
    
    from .plannedLessonGQLModel import planned_lesson_by_id
    
    planned_lesson_by_id = planned_lesson_by_id
    
    from .plannedLessonGQLModel import planned_lesson_page
    
    planned_lesson_page = planned_lesson_page
    
    from .plannedLessonGQLModel import planned_lessons_by_semester
    
    planned_lessons_by_semester = planned_lessons_by_semester
    
    from .plannedLessonGQLModel import planned_lessons_by_topic
    
    planned_lessons_by_topic = planned_lessons_by_topic
    
    from .plannedLessonGQLModel import planned_lessons_by_event
    
    planned_lessons_by_event = planned_lessons_by_event