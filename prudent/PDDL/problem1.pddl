(define (problem p)
(:domain dialogplan3)
(:objects
    user_dialogue
) 
(:INIT
    (status-have-user-query user_dialogue)
(status-have-partial-query user_dialogue)
)
(:goal (and (status-display-result user_dialogue))
)
)