(define (problem p0)
(:domain dialogplan3)
(:objects
    user_dialogue
) 
(:INIT  
    (status-unknown-user-query user_dialogue)
)
(:goal (and (status-have-user-query user_dialogue))
)
)